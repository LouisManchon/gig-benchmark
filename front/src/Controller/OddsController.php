<?php

namespace App\Controller;

use App\Entity\Odd;
use App\Form\OddsFilterType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class OddsController extends AbstractController
{
    #[Route('/', name: 'home')]
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, EntityManagerInterface $em): Response
    {
        $repo = $em->getRepository(Odd::class);

        // all input filters
        $bookmakers = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.bookmaker')
            ->getQuery()
            ->getResult();
        $bookmakersArray = array_map(fn($b) => $b['bookmaker'], $bookmakers);

        $matches = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.match_name')
            ->getQuery()
            ->getResult();
        $matchesArray = array_map(fn($m) => $m['match_name'], $matches);

        $leagues = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.league')
            ->getQuery()
            ->getResult();
        $leaguesArray = array_map(fn($l) => $l['league'], $leagues);

        // Create form
        $form = $this->createForm(OddsFilterType::class, null, [
            'method' => 'GET',
            'bookmakers' => $bookmakersArray,
            'matches' => $matchesArray,
            'leagues' => $leaguesArray,
        ]);

        $form->handleRequest($request);

        $bookmakerFilter = [];
        $matchFilter = null;
        $leagueFilter = null;
        $dateRange = null;

        if ($form->isSubmitted() && $form->isValid()) {
            $bookmakerFilter = $form->get('bookmaker')->getData() ?? [];
            $matchFilter = $form->get('match')->getData();
            $leagueFilter = $form->get('league')->getData();
            $dateRange = $form->get('dateRange')->getData();

            if (is_array($bookmakerFilter) && in_array('all', $bookmakerFilter)) {
                $bookmakerFilter = [];
            }
        }

        // QueryBuilder with filters
        $qb = $repo->createQueryBuilder('o');

        if (!empty($bookmakerFilter)) {
            $qb->andWhere('o.bookmaker IN (:bookmakers)')
               ->setParameter('bookmakers', $bookmakerFilter);
        }

        if ($leagueFilter && $leagueFilter !== 'all') {
            $qb->andWhere('o.league = :league')
               ->setParameter('league', $leagueFilter);
        }

        if ($matchFilter && $matchFilter !== 'all') {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $matchFilter);
        }

        if ($dateRange) {
            // Flatpickr renvoie "YYYY-MM-DD to YYYY-MM-DD"
            if (str_contains($dateRange, ' to ')) {
                $dates = explode(' to ', $dateRange);
            } elseif (str_contains($dateRange, ' à ')) {
                $dates = explode(' à ', $dateRange);
            } else {
                $dates = [$dateRange];
            }

            try {
                $start = new \DateTime(trim($dates[0]) . ' 00:00:00');
                $end = isset($dates[1])
                    ? new \DateTime(trim($dates[1]) . ' 23:59:59')
                    : new \DateTime(trim($dates[0]) . ' 23:59:59');

                $qb->andWhere('o.matchDate BETWEEN :start AND :end')
                   ->setParameter('start', $start)
                   ->setParameter('end', $end);
            } catch (\Exception $e) {
                // ignore
            }
        }

        $qb->orderBy('o.createdAt', 'DESC');
        $allOdds = $qb->getQuery()->getResult();

        // Latest odds par match + bookmaker
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }

        // evolution TRJ

        $oddsWithEvolution = [];
        foreach ($latestOdds as $key => $currentOdd) {
            // Récupérer le TRJ précédent (avant le dernier scraping)
            $previousOdd = $repo->createQueryBuilder('o')
                ->where('o.match_name = :match')
                ->andWhere('o.bookmaker = :bookmaker')
                ->andWhere('o.createdAt < :currentDate')
                ->setParameter('match', $currentOdd->getMatchName())
                ->setParameter('bookmaker', $currentOdd->getBookmaker())
                ->setParameter('currentDate', $currentOdd->getCreatedAt())
                ->orderBy('o.createdAt', 'DESC')
                ->setMaxResults(1)
                ->getQuery()
                ->getOneOrNullResult();

            $evolution = 0; // 0 = stable, 1 = hausse, -1 = baisse
            if ($previousOdd) {
                $diff = $currentOdd->getTrj() - $previousOdd->getTrj();
                if ($diff > 0.1) {
                    $evolution = 1; // hausse
                } elseif ($diff < -0.1) {
                    $evolution = -1; // baisse
                }
            }

            $oddsWithEvolution[] = [
                'odd' => $currentOdd,
                'evolution' => $evolution
            ];
        }

        // Avg TRJ by bookmaker
        $avgQb = $repo->createQueryBuilder('o')
            ->select('o.bookmaker, AVG(o.trj) AS avgTrj')
            ->groupBy('o.bookmaker');

        if (!empty($bookmakerFilter)) {
            $avgQb->andWhere('o.bookmaker IN (:bookmakers)')
                   ->setParameter('bookmakers', $bookmakerFilter);
        }
        if ($leagueFilter && $leagueFilter !== 'all') {
            $avgQb->andWhere('o.league = :league')
                   ->setParameter('league', $leagueFilter);
        }
        if ($matchFilter && $matchFilter !== 'all') {
            $avgQb->andWhere('o.match_name = :match')
                   ->setParameter('match', $matchFilter);
        }
        if (isset($start) && isset($end)) {
            $avgQb->andWhere('o.matchDate BETWEEN :start AND :end')
                   ->setParameter('start', $start)
                   ->setParameter('end', $end);
        }

        $avgTrj = $avgQb->getQuery()->getResult();
        

        // add avgtrj with evolution

       $avgTrjWithEvolution = [];
        
        // Récupérer la date du dernier scraping
        $lastScrapingDate = $repo->createQueryBuilder('o')
            ->select('MAX(o.createdAt)')
            ->getQuery()
            ->getSingleScalarResult();
        
        // Récupérer la date de l'avant-dernier scraping
        $previousScrapingDate = $repo->createQueryBuilder('o')
            ->select('MAX(o.createdAt)')
            ->where('o.createdAt < :lastDate')
            ->setParameter('lastDate', $lastScrapingDate)
            ->getQuery()
            ->getSingleScalarResult();
        
        foreach ($avgTrj as $row) {
            $evolution = 0;
            
            if ($previousScrapingDate) {
                // TRJ moyen de ce bookmaker lors du scraping précédent
                $previousAvg = $repo->createQueryBuilder('o')
                    ->select('AVG(o.trj) AS avgTrj')
                    ->where('o.bookmaker = :bookmaker')
                    ->andWhere('o.createdAt = :previousDate')
                    ->setParameter('bookmaker', $row['bookmaker'])
                    ->setParameter('previousDate', $previousScrapingDate)
                    ->getQuery()
                    ->getOneOrNullResult();

                if ($previousAvg && $previousAvg['avgTrj']) {
                    $diff = $row['avgTrj'] - $previousAvg['avgTrj'];
                    if ($diff > 0.1) {
                        $evolution = 1;
                    } elseif ($diff < -0.1) {
                        $evolution = -1;
                    }
                }
            }

            $avgTrjWithEvolution[] = [
                'bookmaker' => $row['bookmaker'],
                'avgTrj' => $row['avgTrj'],
                'evolution' => $evolution
            ];
        }

        // Render
        return $this->render('odds/index.html.twig', [
            'form' => $form->createView(),
            'odds' => $latestOdds,
            'avgTrj' => $avgTrj
        ]);
    }
}