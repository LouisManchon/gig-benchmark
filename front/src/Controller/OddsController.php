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

        // 2️⃣ Créer le formulaire
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

        // 🔧 FIX ICI : utilise get() au lieu de getData()
        if ($form->isSubmitted() && $form->isValid()) {
            $bookmakerFilter = $form->get('bookmaker')->getData() ?? [];
            $matchFilter = $form->get('match')->getData();
            $leagueFilter = $form->get('league')->getData();
            $dateRange = $form->get('dateRange')->getData();

            // Si "All" est sélectionné pour Bookmakers
            if (is_array($bookmakerFilter) && in_array('all', $bookmakerFilter)) {
                $bookmakerFilter = [];
            }
        }

        // 3️⃣ Construire QueryBuilder avec filtres
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
                // Ignorer ou logger
            }
        }

        $qb->orderBy('o.createdAt', 'DESC');
        $allOdds = $qb->getQuery()->getResult();

        // 4️⃣ Latest odds par match + bookmaker
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }

        // 5️⃣ Avg TRJ par bookmaker
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
        $chartLabels = array_map(fn($r) => $r['bookmaker'], $avgTrj);
        $chartData = array_map(fn($r) => (float) $r['avgTrj'], $avgTrj);

        // 6️⃣ Rendu
        return $this->render('odds/index.html.twig', [
            'form' => $form->createView(),
            'odds' => $latestOdds,
            'avgTrj' => $avgTrj,
            'chartLabels' => $chartLabels,
            'chartData' => $chartData,
        ]);
    }
}