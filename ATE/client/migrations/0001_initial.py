# Generated by Django 3.2.8 on 2022-02-09 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_level', models.CharField(choices=[('diploma', 'College/diploma'), ('undergraduate', 'Undergraduate'), ('Masters', 'Masters'), ('Phd', 'Phd')], max_length=20)),
                ('type_of_paper', models.CharField(choices=[('Essay', 'Essay (Any Type)'), ('Abstract', 'Abstract'), ('admission Essay', 'Admission Essay'), ('Annotated Bibliography', 'Annotated Bibliography'), ('Argumentative Essay', 'Argumentative Essay'), ('Article (Any Type)', 'Article (Any Type)'), ('Article Review', 'Article Review'), ('Article Summary', 'Article Summary'), ('Assessment', 'Assessment'), ('Book report', 'Book Report'), ('Book review', 'Book Review'), ('Book/Movie Review', 'Book/Movie Review'), ('Breafing paper', 'Breafing Paper'), ('Business Plan', 'Business Plan'), ('Capstone project', 'Capstone Project'), ('Cases Study', 'Cases Study'), ('Content (Any Type)', 'Content (Any Type)'), ('Coursework', 'Coursework'), ('Cover letter', 'Cover Letter'), ('Creative writing', 'Creative Writing'), ('Critical thinking', 'Critical Thinking'), ('data analysis', 'Data Analysis'), ('Design paper', 'Design Paper'), ('Dissertation', 'Dissertation'), ('Editing/Proofreading', 'Editing/Proofreading'), ('Essay', 'Essay'), ('Executive Summary', 'Executive Summary'), ('Finance Excel Analysis', 'Finance Excel Analysis'), ('Financial Analysis', 'Financial Analysis'), ('Financial Statments', 'Financial Statments'), ('Journal Article', 'Journal Article'), ('Journal Entry', 'Journal Entry'), ('Lab report', 'Lab Report'), ('Literature Review', 'Literature Review'), ('Marketing Plan', 'Marketing Plan'), ('Math Problem', 'Math Problem'), ('Mind concept-map', 'Mind Concept-Map'), ('Movie review', 'Movie Review'), ('Multiple choices', 'Multiple Choices'), ('Online Assignment', 'Online Assignment'), ('other (Not listed)', 'other (Not listed)'), ('PDF poster', 'PDF Poster'), ('PESTLE Analysis', 'PESTLE Analysis'), ('Phys/Econ/Fin/Stat Problems', 'Phys/Econ/Fin/Stat Problems'), ('Presentation', 'Presentation'), ('Psychology Report', 'Psychology Report'), ('Q&A', 'Q&A'), ('Reaction Paper', 'Reaction Paper'), ('Report', 'Report'), ('Research Design/Methodology', 'Research Design/Methodology'), ('Research Paper', 'Research Paper'), ('Research proposal', 'Research Proposal'), ('Research Summary', 'Research Summary'), ('Resume/CV', 'Resume/CV'), ('Rewriting', 'Rewriting'), ('Scholarship Essay', 'Scholarship Essay'), ('Short Answers', 'Short Answers'), ('Speech', 'Speech'), ('Speech Work', 'Speech Work'), ('Statstic Project', 'Statstic Project'), ('SWOT Analysis', 'SWOT Analysis'), ('Term Paper', 'Term Paper'), ('Thesis', 'Thesis'), ('Thesis/Dissertation - Discussion', 'Thesis/Dissertation - Discussion'), ('Thesis/Dissertation - Abstract', 'Thesis/Dissertation - Abstract'), ('Thesis/Dissertation - Conclusion', 'Thesis/Dissertation - Conclusion'), ('Thesis/Dissertation - Introduction', 'Thesis/Dissertation - Introduction'), ('Thesis/Dissertation - Literature Review', 'Thesis/Dissertation - Literature Review'), ('Thesis/Dissertation - Methodology', 'Thesis/Dissertation - Methodology'), ('Thesis/Dissertation - Outline/Form', 'Thesis/Dissertation - Outline/Form'), ('Thesis/Dissertation - Results', 'Thesis/Dissertation - Results'), ('Thesis/Dissertation Proposal', 'Thesis/Dissertation Proposal')], max_length=50)),
                ('subject_area', models.CharField(choices=[('Accounting', 'Accounting'), ('Aeronautics', 'Aeronautics'), ('Anthropology', 'Anthropology'), ('Archeology', 'Archeology'), ('Architecture', 'Architecture'), ('Arts', 'Arts'), ('Astronomy', 'Astronomy'), ('Auditing', 'Auditing'), ('Aviation', 'Aviation'), ('Bio-Medical Sciences', 'Bio-Medical Sciences'), ('Biochemistry', 'Biochemistry'), ('Biology', 'Biology'), ('Building & Construction', 'Building & Construction'), ('Business', 'Business'), ('Chemistry', 'Chemistry'), ('Childcare', 'Childcare'), ('Communication and Media', 'Communication and Media'), ('Company Analysis', 'Company Analysis'), ('Computers', 'Computers'), ('Counseling', 'Counseling'), ('Criminology', 'Criminology'), ('Economics', 'Economics'), ('Education', 'Education'), ('Engineering', 'Engineering'), ('English', 'English'), ('Environmental-Studies', 'Environmental-Studies'), ('Ethics', 'Ethics'), ('Ethnic-Studies', 'Ethnic-Studies'), ('finance', 'finance'), ('Food-Nutrition', 'Food-Nutrition'), ('Geography', 'Geography'), ('Geology', 'Geology'), ('Healthcare', 'Healthcare'), ('History', 'History'), ('Internet', 'Internet'), ('Investment', 'Investment'), ('IT Management', 'IT Management'), ('Law', 'Law'), ('Legal Issues', 'Legal Issues'), ('Linguistics', 'Linguistics'), ('Literature', 'Literature'), ('Logistics', 'Logistics'), ('Management', 'Management'), ('Marketing', 'Marketing'), ('Mathematics', 'Mathematics'), ('Medicine', 'Medicine'), ('Military Studies', 'Military Studies'), ('Music', 'Music'), ('Nursing', 'Nursing'), ('Nutrition', 'Nutrition'), ('Other(Not Listed)', 'Other(Not Listed)'), ('Pedagogy', 'Pedagogy'), ('Pharmacology', 'Pharmacology'), ('Philosophy', 'Philosophy'), ('Physical-Education', 'Physical-Education'), ('Physics', 'Physics'), ('Physical Problems', 'Physical Problems'), ('Political Science', 'Political Science'), ('Politics', 'Politics'), ('Procurement', 'Procurement'), ('Psychology', 'Psychology'), ('Quantity Survey', 'Quantity Survey'), ('Religion', 'Religion'), ('Sociology', 'Sociology'), ('Sport', 'Sport'), ('Statistics', 'Statistics'), ('Taxation Theory, Practice & Law', 'Taxation Theory, Practice & Law'), ("Teacher's Career", "Teacher's Career"), ('Tourism', 'Tourism'), ('Trade', 'Trade')], max_length=50)),
                ('title', models.CharField(max_length=250)),
                ('paper_instructions', models.TextField()),
                ('Additional_materials', models.FileField(blank=True, help_text='Please upload any additional files here! ZIP multiple files', null=True, upload_to='')),
                ('paper_format', models.CharField(choices=[('APA', 'APA'), ('MLA', 'MLA'), ('Harvard', 'Harvard'), ('Other', 'Other'), ('OSCOLA', 'OSCOLA'), ('AGLC', 'AGLC'), ('Chicago', 'Chicago'), ('Oxford', 'Oxford')], max_length=50)),
                ('number_of_pages', models.IntegerField(help_text='0 words approx')),
                ('spacing', models.CharField(choices=[('single', 'Single spaced'), ('double', 'Double spaced')], max_length=50)),
                ('currency', models.CharField(default='$', help_text='currency is always in US dollars', max_length=50)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, help_text="This is an automatically generated field, don't fill in")),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('complete', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('price', models.FloatField(default=0.0, help_text='This field is auto-generated hence cannot be changed')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]
