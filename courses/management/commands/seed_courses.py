from decimal import Decimal

from django.core.management.base import BaseCommand

from courses.models import Category, Course


COURSES = [
    {
        'category': ('Market Structure', 'market-structure'),
        'title': 'Market Structure Foundations',
        'slug': 'market-structure-foundations',
        'summary': 'Build an objective language for trends, corrections and invalidation.',
        'description': (
            'A practical introduction to reading price through swing structure. '
            'You will learn to separate observation from prediction and create '
            'a repeatable pre-trade map.'
        ),
        'learning_outcomes': (
            'Identify higher-high and lower-low sequences\n'
            'Separate trending and corrective conditions\n'
            'Define a clear structural invalidation point'
        ),
        'lesson_content': (
            'Lesson 1: Describe before you predict\n\n'
            'Start every chart review by recording only observable swings. '
            'Label direction, the most recent confirmed swing and the price '
            'that would invalidate the current structural idea.\n\n'
            'Lesson 2: Trend and correction\n\n'
            'A trend advances through directional legs and pauses through '
            'corrections. Your job is to recognize which condition is present '
            'and avoid forcing a trend entry inside unclear structure.\n\n'
            'Practice: capture three charts and write a one-sentence structural '
            'description for each before noting any trade idea.'
        ),
        'level': 'beginner',
        'price': Decimal('39.00'),
    },
    {
        'category': ('Risk Management', 'risk-management'),
        'title': 'Risk Before Reward',
        'slug': 'risk-before-reward',
        'summary': 'Turn account protection into a repeatable position-sizing process.',
        'description': (
            'Learn how invalidation distance, account risk and contract value '
            'work together before an order is placed.'
        ),
        'learning_outcomes': (
            'Calculate risk per trade before entry\n'
            'Match position size to invalidation distance\n'
            'Create daily and weekly loss boundaries'
        ),
        'lesson_content': (
            'Lesson 1: The loss is defined first\n\n'
            'A valid setup is not automatically a valid risk. Determine the '
            'distance from entry to invalidation, translate it into currency '
            'risk and reduce size when it exceeds your plan.\n\n'
            'Lesson 2: Protect decision quality\n\n'
            'Daily loss boundaries prevent one difficult session from becoming '
            'a destructive week. Stop trading when the boundary is reached and '
            'review the process away from the live chart.\n\n'
            'Practice: write a position-sizing example for three different stop '
            'distances while keeping total account risk constant.'
        ),
        'level': 'beginner',
        'price': Decimal('49.00'),
    },
    {
        'category': ('Trading Process', 'trading-process'),
        'title': 'Execution Discipline',
        'slug': 'execution-discipline',
        'summary': 'Design a pre-session and post-session routine you can measure.',
        'description': (
            'Build a simple operating process around preparation, execution and '
            'review so that progress is based on evidence rather than emotion.'
        ),
        'learning_outcomes': (
            'Build a concise pre-session checklist\n'
            'Record rule adherence separately from profit\n'
            'Use review data to choose one improvement at a time'
        ),
        'lesson_content': (
            'Lesson 1: A checklist protects attention\n\n'
            'Your checklist should contain only decisions required before an '
            'entry: market condition, setup, invalidation, size and planned '
            'management. If one item is unknown, there is no trade yet.\n\n'
            'Lesson 2: Grade the decision\n\n'
            'Profit does not prove that a decision was good, and a controlled '
            'loss does not prove it was bad. Review whether every planned rule '
            'was followed, then record one specific improvement.\n\n'
            'Practice: review five trades and assign separate scores for process '
            'quality and financial outcome.'
        ),
        'level': 'intermediate',
        'price': Decimal('59.00'),
    },
]


class Command(BaseCommand):
    help = 'Create or update the academy demonstration course catalogue.'

    def handle(self, *args, **options):
        for data in COURSES:
            category_name, category_slug = data['category']
            category, _ = Category.objects.get_or_create(
                slug=category_slug, defaults={'name': category_name})
            defaults = {**data, 'category': category, 'is_published': True}
            Course.objects.update_or_create(
                slug=data['slug'], defaults=defaults)
        self.stdout.write(self.style.SUCCESS('Academy courses are ready.'))
