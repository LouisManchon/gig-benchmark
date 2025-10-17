<?php

namespace App\Repository;

use App\Entity\Odd;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class OddRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Odd::class);
    }

    // Récupère les valeurs distinctes pour les filtres
    public function findDistinctBookmakers(): array
    {
        return array_map(
            fn($b) => $b['bookmaker'],
            $this->createQueryBuilder('o')
                ->select('DISTINCT o.bookmaker')
                ->getQuery()
                ->getResult()
        );
    }

    public function findDistinctMatches(): array
    {
        return array_map(
            fn($m) => $m['match_name'],
            $this->createQueryBuilder('o')
                ->select('DISTINCT o.match_name')
                ->getQuery()
                ->getResult()
        );
    }

    public function findDistinctLeagues(): array
    {
        return array_map(
            fn($l) => $l['league'],
            $this->createQueryBuilder('o')
                ->select('DISTINCT o.league')
                ->getQuery()
                ->getResult()
        );
    }

    // Requête filtrée par bookmaker, match, league et date
    public function findWithFilters(array $bookmakers = [], ?string $league = null, ?string $match = null, ?\DateTime $start = null, ?\DateTime $end = null): array
    {
        $qb = $this->createQueryBuilder('o');

        if (!empty($bookmakers)) {
            $qb->andWhere('o.bookmaker IN (:bookmakers)')
               ->setParameter('bookmakers', $bookmakers);
        }

        if ($league && $league !== 'all') {
            $qb->andWhere('o.league = :league')
               ->setParameter('league', $league);
        }

        if ($match && $match !== 'all') {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $match);
        }

        if ($start && $end) {
            $qb->andWhere('o.matchDate BETWEEN :start AND :end')
               ->setParameter('start', $start)
               ->setParameter('end', $end);
        }

        $qb->orderBy('o.createdAt', 'DESC');

        return $qb->getQuery()->getResult();
    }

    // Récupérer le TRJ précédent pour un match et bookmaker donné
    public function findPreviousOdd(string $matchName, string $bookmaker, \DateTimeInterface $currentDate): ?Odd
    {
        return $this->createQueryBuilder('o')
            ->where('o.match_name = :match')
            ->andWhere('o.bookmaker = :bookmaker')
            ->andWhere('o.createdAt < :currentDate')
            ->setParameter('match', $matchName)
            ->setParameter('bookmaker', $bookmaker)
            ->setParameter('currentDate', $currentDate)
            ->orderBy('o.createdAt', 'DESC')
            ->setMaxResults(1)
            ->getQuery()
            ->getOneOrNullResult();
    }

    // Moyenne TRJ par bookmaker avec filtres
    public function findAvgTrj(array $bookmakers = [], ?string $league = null, ?string $match = null, ?\DateTime $start = null, ?\DateTime $end = null): array
    {
        $qb = $this->createQueryBuilder('o')
            ->select('o.bookmaker, AVG(o.trj) AS avgTrj')
            ->groupBy('o.bookmaker');

        if (!empty($bookmakers)) {
            $qb->andWhere('o.bookmaker IN (:bookmakers)')
               ->setParameter('bookmakers', $bookmakers);
        }

        if ($league && $league !== 'all') {
            $qb->andWhere('o.league = :league')
               ->setParameter('league', $league);
        }

        if ($match && $match !== 'all') {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $match);
        }

        if ($start && $end) {
            $qb->andWhere('o.matchDate BETWEEN :start AND :end')
               ->setParameter('start', $start)
               ->setParameter('end', $end);
        }

        return $qb->getQuery()->getResult();
    }

    // Récupérer la date du dernier scraping (jour uniquement)
    public function findLastScrapingDate(): ?\DateTimeInterface
    {
        $result = $this->createQueryBuilder('o')
            ->select('o.createdAt')
            ->orderBy('o.createdAt', 'DESC')
            ->setMaxResults(1)
            ->getQuery()
            ->getSingleScalarResult();

        return $result ? new \DateTime($result) : null;
    }

    // Récupérer la date de l'avant-dernier scraping (jour uniquement)
    public function findPreviousScrapingDate(\DateTimeInterface $lastDate): ?\DateTimeInterface
    {
        // Crée une date juste avant $lastDate pour exclure cette dernière
        $lastDateClone = (clone $lastDate)->setTime(0, 0, 0);

        $result = $this->createQueryBuilder('o')
            ->select('o.createdAt')
            ->where('o.createdAt < :lastDate')
            ->setParameter('lastDate', $lastDateClone)
            ->orderBy('o.createdAt', 'DESC')
            ->setMaxResults(1)
            ->getQuery()
            ->getSingleScalarResult();

        return $result ? new \DateTime($result) : null;
    }


    // Récupère le TRJ moyen du bookmaker lors de l'avant-dernier scraping
    public function findPreviousAvgForBookmaker(string $bookmaker): ?float
    {
        // Trouve les 2 dernières dates de scraping pour ce bookmaker
        $dates = $this->createQueryBuilder('o')
            ->select('DISTINCT o.createdAt')
            ->where('o.bookmaker = :bookmaker')
            ->setParameter('bookmaker', $bookmaker)
            ->orderBy('o.createdAt', 'DESC')
            ->setMaxResults(2)
            ->getQuery()
            ->getResult();

        // S'il n'y a pas au moins 2 scrapings, on retourne null
        if (count($dates) < 2) {
            return null;
        }

        // Prend la 2ème date (avant-dernier scraping)
        $previousDate = $dates[1]['createdAt'];

        // Calcule la moyenne pour ce bookmaker à cette date précise
        $result = $this->createQueryBuilder('o')
            ->select('AVG(o.trj) as avgTrj')
            ->where('o.bookmaker = :bookmaker')
            ->andWhere('o.createdAt = :date')
            ->setParameter('bookmaker', $bookmaker)
            ->setParameter('date', $previousDate)
            ->getQuery()
            ->getSingleScalarResult();

        return $result ? (float) $result : null;
    }
}
