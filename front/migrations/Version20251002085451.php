<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20251002085451 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('CREATE TABLE messenger_messages (id BIGINT AUTO_INCREMENT NOT NULL, body LONGTEXT NOT NULL, headers LONGTEXT NOT NULL, queue_name VARCHAR(190) NOT NULL, created_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', available_at DATETIME NOT NULL COMMENT \'(DC2Type:datetime_immutable)\', delivered_at DATETIME DEFAULT NULL COMMENT \'(DC2Type:datetime_immutable)\', INDEX IDX_75EA56E0FB7336F0 (queue_name), INDEX IDX_75EA56E0E3BD61CE (available_at), INDEX IDX_75EA56E016BA31DB (delivered_at), PRIMARY KEY(id)) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_unicode_ci` ENGINE = InnoDB');
        $this->addSql('ALTER TABLE cotes CHANGE match_name match_name VARCHAR(255) NOT NULL, CHANGE bookmaker bookmaker VARCHAR(100) NOT NULL, CHANGE cote_1 cote_1 DOUBLE PRECISION NOT NULL, CHANGE cote_N cote_n DOUBLE PRECISION NOT NULL, CHANGE cote_2 cote_2 DOUBLE PRECISION NOT NULL, CHANGE created_at created_at DATETIME NOT NULL');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('DROP TABLE messenger_messages');
        $this->addSql('ALTER TABLE cotes CHANGE match_name match_name VARCHAR(255) DEFAULT NULL, CHANGE bookmaker bookmaker VARCHAR(100) DEFAULT NULL, CHANGE cote_1 cote_1 VARCHAR(10) DEFAULT NULL, CHANGE cote_n cote_N VARCHAR(10) DEFAULT NULL, CHANGE cote_2 cote_2 VARCHAR(10) DEFAULT NULL, CHANGE created_at created_at DATETIME DEFAULT CURRENT_TIMESTAMP');
    }
}
