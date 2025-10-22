<?php

// src/Form/Type/BookmakerType.php
namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class BookmakerType extends AbstractType
{
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'choices' => [],       // liste des bookmakers
            'include_all' => true, // ajouter "All" par défaut
            'multiple' => true,    // multi-select
        ]);
    }

    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $choices = $options['choices'];
        if ($options['include_all']) {
            $choices = array_merge(['All' => 'all'], $choices);
        }

        $builder->add('bookmaker', ChoiceType::class, [
            'choices' => array_merge(['All' => 'all'], array_combine($options['bookmakers'], $options['bookmakers'])),
            'multiple' => $options['multiple'],
            'expanded' => false,  // true = cases visibles, false = select
            'attr' => ['class' => 'form-control'],
        ]);
    }
}
