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

        $repo = $em->getRepository(Odd::class);
        $qb = $repo->createQueryBuilder('o');

        // Appliquer les filtres si définis
        if ($bookmakerFilter) {
            $qb->andWhere('o.bookmaker = :bookmaker')
               ->setParameter('bookmaker', $bookmakerFilter);
        }
        if ($matchFilter) {
            $qb->andWhere('o.match_name = :match')
               ->setParameter('match', $matchFilter);
        }

        // Trier par date de création décroissante
        $qb->orderBy('o.createdAt', 'DESC');
        $allOdds = $qb->getQuery()->getResult();

        // Garde uniquement la dernière cote par match + bookmaker
        $latestOdds = [];
        foreach ($allOdds as $odd) {
            $key = $odd->getMatchName() . '|' . $odd->getBookmaker();
            if (!isset($latestOdds[$key])) {
                $latestOdds[$key] = $odd;
            }
        }


        // Récupérer tous les bookmakers et matchs pour les filtres
        $bookmakers = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.bookmaker')
            ->getQuery()
            ->getResult();

        $matches = $repo->createQueryBuilder('o')
            ->select('DISTINCT o.match_name')
            ->getQuery()
            ->getResult();

        return $this->render('odds/index.html.twig', [
            'odds' => $latestOdds,
            'bookmakers' => array_map(fn($b) => $b['bookmaker'], $bookmakers),
            'matches' => array_map(fn($m) => $m['match_name'], $matches),
            'currentBookmaker' => $bookmakerFilter,
            'currentMatch' => $matchFilter,
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
