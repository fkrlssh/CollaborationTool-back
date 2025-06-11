from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [

        migrations.RunPython(code=lambda apps, schema_editor: None, reverse_code=lambda apps, schema_editor: None),
    ]