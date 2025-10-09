<?php

namespace App\Controller;

use App\Entity\Odd;
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
        $bookmakerFilter = $request->query->get('bookmaker');
        $matchFilter = $request->query->get('match');
        $dateFilter = $request->query->get('date');
        $leagueFilter = $request->query->get('league');

        $repo = $em->getRepository(Odd::class);
        $qb = $repo->createQueryBuilder('o');

        // apply filters 
        if ($bookmakerFilter) {
            $qb->andWhere('o.bookmaker = :bookmaker')
               ->setParameter('bookmaker', $bookmakerFilter);
        }
        if ($matchFilter) {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $matchFilter);
        }

        if ($dateFilter) {
            $dateStart = new \DateTime($dateFilter . ' 00:00:00');
            $dateEnd = new \DateTime($dateFilter . ' 23:59:59');

            $qb->andWhere('o.matchDate BETWEEN :start AND :end')
            ->setParameter('start', $dateStart)
            ->setParameter('end', $dateEnd);
        }


        // desc
        $qb->orderBy('o.createdAt', 'DESC');
        $allOdds = $qb->getQuery()->getResult();

        // latest odds
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }


        // all bookmakers and matchs
        $bookmakers = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.bookmaker')
            ->getQuery()
            ->getResult();

        $matches = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.match_name')
            ->getQuery()
            ->getResult();

        $leagues = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.league')
            ->getQuery()
            ->getResult();
        
        $avgTrj = $repo->createQueryBuilder('o')
            ->select('o.bookmaker, AVG(o.trj) AS avgTrj')
            ->groupBy('o.bookmaker')
            ->getQuery()
            ->getResult();

        return $this->render('odds/index.html.twig', [
            'odds' => $latestOdds,
            'bookmakers' => array_map(fn($b) => $b['bookmaker'], $bookmakers),
            'matches' => array_map(fn($m) => $m['match_name'], $matches),
            'leagues' => array_map(fn($l) => $l['league'], $leagues),
            'currentBookmaker' => $bookmakerFilter,
            'currentMatch' => $matchFilter,
            'currentLeague' => $leagueFilter,
            'currentDate' => $dateFilter,
            'avgTrj' => $avgTrj
        ]);
    }

    #[Route('/odds/scrape', name: 'odds_scrape', methods: ['POST'])]
    public function scrape(): Response
    {
        // Connexion à RabbitMQ
        $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $connection->channel();
        $channel->queue_declare('cotes', false, false, false, false);

        // Envoi d'un message pour déclencher le scraping
        $msg = new AMQPMessage(json_encode(['action' => 'scrape']));
        $channel->basic_publish($msg, '', 'cotes');

        $channel->close();
        $connection->close();

        $this->addFlash('success', 'Scraping OK');

        return $this->redirectToRoute('odds_list');
    }
}
