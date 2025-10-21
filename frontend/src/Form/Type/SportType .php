<?php

// src/Form/Type/MatchType.php
namespace App\Form\Type;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class MatchType extends AbstractType
{
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'choices' => [],
            'include_all' => true,
        ]);
    }

    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $choices = $options['choices'];
        if ($options['include_all']) {
            $choices = array_merge(['All' => 'all'], $choices);
        }

        $builder->add('match', ChoiceType::class, [
            'choices' => array_combine($choices, $choices),
            'multiple' => false,
            'expanded' => false,
            'attr' => ['class' => 'form-control'],
        ]);
    }
}
