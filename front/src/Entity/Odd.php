<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: "odds")]
class Odd
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: "integer")]
    private int $id;

    #[ORM\Column(type: "string", length: 255)]
    private string $match_name;

    #[ORM\Column(type: "string", length: 100)]
    private string $bookmaker;

    #[ORM\Column(type: "float", nullable: true)]
    private ?float $cote_1 = null;

    #[ORM\Column(type: "float", nullable: true)]
    private ?float $cote_N = null;

    #[ORM\Column(type: "float", nullable: true)]
    private ?float $cote_2 = null;

    #[ORM\Column(type:"float", nullable: true)]
    private ?float $trj = null;

    #[ORM\Column(type:"string")]
    private string $league;

    #[ORM\Column(type: "datetime")]
    private \DateTimeInterface $createdAt;

    #[ORM\Column(type: 'datetime', nullable: true)]
    private ?\DateTimeInterface $matchDate = null;


    // Getters and setters

    public function getId(): int
    {
        return $this->id;
    }

    public function getMatchName(): string
    {
        return $this->match_name;
    }

    public function setMatchName(string $match_name): self
    {
        $this->match_name = $match_name;
        return $this;
    }

    public function getBookmaker(): string
    {
        return $this->bookmaker;
    }

    public function setBookmaker(string $bookmaker): self
    {
        $this->bookmaker = $bookmaker;
        return $this;
    }

    public function getCote1(): ?float
    {
        return $this->cote_1;
    }

    public function setCote1(float $cote_1): self
    {
        $this->cote_1 = $cote_1;
        return $this;
    }

    public function getCoteN(): ?float
    {
        return $this->cote_N;
    }

    public function setCoteN(float $cote_N): self
    {
        $this->cote_N = $cote_N;
        return $this;
    }

    public function getCote2(): ?float
    {
        return $this->cote_2;
    }

    public function setCote2(float $cote_2): self
    {
        $this->cote_2 = $cote_2;
        return $this;
    }

    public function getLeague(): string
    {
        return $this->league;
    }

    public function setLeague(string $League)
    {
        $this->$league = $league;
        return $this;
    }

    public function getCreatedAt(): ?\DateTimeInterface
    {
        return $this->createdAt;
    }

    public function setCreatedAt(\DateTimeInterface $createdAt): self
    {
        $this->createdAt = $createdAt;
        return $this;
    }

    public function __construct()
    {
        $this->createdAt = new \DateTimeImmutable();
    }

    public function getTrj(): ?float
    {
      return $this->trj;
    }

    public function setTrj()
    {
      $this->trj = $trj;
      return $this;
    }

    public function getMatchDate(): ?\DateTimeInterface
    {
        return $this->matchDate;
    }

    public function setMatchDate(?\DateTimeInterface $matchDate): self
    {
        $this->matchDate = $matchDate;
        return $this;
    }

}
