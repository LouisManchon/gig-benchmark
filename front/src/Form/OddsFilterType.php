<?php

namespace App\Form;

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class OddsFilterType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('bookmaker', ChoiceType::class, [
                'choices' => array_merge(
                    ['All' => 'all'], 
                    array_combine($options['bookmakers'], $options['bookmakers'])
                ),
                'data' => ['all'], // 🔧 Valeur par défaut
                'required' => false,
                'multiple' => true,
                'expanded' => false,
                'attr' => ['class' => 'js-bookmaker-select']
            ])
            ->add('league', ChoiceType::class, [
                'choices' => array_combine($options['leagues'], $options['leagues']),
                'placeholder' => 'All',
                'required' => false
            ])
            ->add('match', ChoiceType::class, [
                'choices' => array_combine($options['matches'], $options['matches']),
                'placeholder' => 'All',
                'required' => false
            ])
            ->add('dateRange', TextType::class, [
                'required' => false,
                'attr' => ['class' => 'js-date-range']
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'bookmakers' => [],
            'matches' => [],
            'leagues' => [],
            'data_class' => null,
        ]);
    }
}
