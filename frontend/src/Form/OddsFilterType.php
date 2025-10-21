<?php

namespace App\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class OddsFilterType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('sport', ChoiceType::class, [
                'choices' => $options['sports'],
                'required' => false,
                'placeholder' => 'All sports',  // ✅ Placeholder
                'attr' => [
                    'class' => 'form-control',
                    'data-filter' => 'sport'  // ✅ Pour JS
                ],
                'label' => 'Sport'
            ])
            ->add('league', ChoiceType::class, [
                'choices' => $options['leagues'],
                'multiple' => true,
                'expanded' => false,
                'required' => false,
                'placeholder' => 'All leagues',
                'attr' => [
                    'class' => 'form-control',
                    'data-filter' => 'league',
                    'data-placeholder' => 'All leagues'
                ],
                'label' => 'League'
            ])
            ->add('bookmaker', ChoiceType::class, [
                'choices' => $options['bookmakers'],
                'multiple' => true,
                'expanded' => false,
                'required' => false,
                'placeholder' => 'All bookmakers',
                'attr' => [
                    'class' => 'form-control',
                    'data-placeholder' => 'All bookmakers'  // ✅ Pour Choices.js
                ],
                'label' => 'Bookmaker'
            ])
            ->add('match', ChoiceType::class, [
                'choices' => $options['matches'],
                'required' => false,
                'placeholder' => 'All matches',
                'attr' => ['class' => 'form-control'],
                'label' => 'Match'
            ])
            ->add('dateRange', TextType::class, [
                'required' => false,
                'attr' => [
                    'class' => 'form-control js-date-range',
                    'placeholder' => 'Select date range'
                ],
                'label' => 'Date Range'
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'sports' => [],
            'bookmakers' => [],
            'leagues' => [],
            'matches' => [],
            'method' => 'GET',
            'csrf_protection' => false,
        ]);
    }
}
