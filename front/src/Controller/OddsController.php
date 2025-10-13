<?php

namespace App\Controller;

use App\Entity\Odd;
use App\Form\OddsFilterType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Process\Process;
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;


class OddsController extends AbstractController
{
    #[Route('/', name: 'home')]
    #[Route('/odds', name: 'odds_list')]
    public function index(Request $request, EntityManagerInterface $em): Response
    {
        $repo = $em->getRepository(Odd::class);

        // 1️⃣ Récupérer tous les choix pour les filtres
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


        // 2️⃣ Créer le formulaire avec les choix récupérés
        $form = $this->createForm(OddsFilterType::class, null, [
            'bookmakers' => $bookmakersArray, // tableau simple ['Bookmaker1', 'Bookmaker2', ...]
            'matches' => $matchesArray,
            'leagues' => $leaguesArray,
        ]);

        $form->handleRequest($request);

        $bookmakerFilter = [];
        $matchFilter = null;
        $leagueFilter = null;
        $dateRange = null;

        // 3️⃣ Récupérer les valeurs filtrées
        if ($form->isSubmitted() && $form->isValid()) {
            $data = $form->getData();
            $bookmakerFilter = $data['bookmaker'] ?? [];
            $matchFilter = $data['match'] ?? null;
            $leagueFilter = $data['league'] ?? null;
            $dateRange = $data['dateRange'] ?? null;
        }

        // Si "All" est sélectionné pour les bookmakers, on ignore le filtre
        if (in_array('all', $bookmakerFilter)) {
            $bookmakerFilter = [];
        }

        // 4️⃣ Construire le QueryBuilder principal
        $qb = $repo->createQueryBuilder('o');

        if (!empty($bookmakerFilter)) {
            $qb->andWhere('o.bookmaker IN (:bookmakers)')
               ->setParameter('bookmakers', $bookmakerFilter);
        }
        if ($matchFilter && $matchFilter !== 'all') {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $matchFilter);
        }
        if ($leagueFilter && $leagueFilter !== 'all') {
            $qb->andWhere('o.league = :league')
               ->setParameter('league', $leagueFilter);
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
                // Ignore ou logger
            }
        }

        $qb->orderBy('o.createdAt', 'DESC');
        $allOdds = $qb->getQuery()->getResult();

        // 5️⃣ Latest odds par match + bookmaker
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }

        // 6️⃣ Avg TRJ avec filtres
        $avgQb = $repo->createQueryBuilder('o')
            ->select('o.bookmaker, AVG(o.trj) AS avgTrj')
            ->groupBy('o.bookmaker');

        if (!empty($bookmakerFilter)) {
            $avgQb->andWhere('o.bookmaker IN (:bookmakers)')
                   ->setParameter('bookmakers', $bookmakerFilter);
        }
        if ($matchFilter && $matchFilter !== 'all') {
            $avgQb->andWhere('o.match_name = :match')
                   ->setParameter('match', $matchFilter);
        }
        if ($leagueFilter && $leagueFilter !== 'all') {
            $avgQb->andWhere('o.league = :league')
                   ->setParameter('league', $leagueFilter);
        }
        if ($dateRange ?? false) {
            $avgQb->andWhere('o.matchDate BETWEEN :start AND :end')
                   ->setParameter('start', $start)
                   ->setParameter('end', $end);
        }

        $avgTrj = $avgQb->getQuery()->getResult();
        $chartLabels = array_map(fn($r) => $r['bookmaker'], $avgTrj);
        $chartData = array_map(fn($r) => (float) $r['avgTrj'], $avgTrj);

        // 7️⃣ Rendu
        return $this->render('odds/index.html.twig', [
            'form' => $form->createView(),
            'odds' => $latestOdds,
            'avgTrj' => $avgTrj,
            'chartLabels' => $chartLabels,
            'chartData' => $chartData,
        ]);
    }

    #[Route('/odds/scrape', name: 'odds_scrape')]
    public function scrape(): Response
    {
        // ton code de scraping ici
    }

}
