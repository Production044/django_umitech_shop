from deep_translator import GoogleTranslator
from threading import Thread, Lock
import logging
from django.db.models import Model

translator = GoogleTranslator('uk', 'en')
logger = logging.getLogger('logit')


lock = Lock()


def translate_product(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.title_en or not obj.description_en:
            Thread(target=translate_product_data, args=(obj,)).start()


translate_product.short_description = 'Translate Product'


def translate_product_data(obj: Model):
    try:
        with lock:
            translate_list = [obj.title, obj.description]
            translated = translator.translate_batch(translate_list)

            obj.title_en = translated[0]
            obj.description_en = translated[1]
            obj.save()
            # logger.info(obj.title_en)

    except Exception as error:
        print(f'{obj.title} {error}')  # заглушка


def translate_name(modeladmin, request, queryset):
    objects_list = []
    for obj in queryset:
        if not obj.name_en:
            objects_list.append(obj)

    Thread(
        target=translate_name_data,
        args=(objects_list, modeladmin.model)
    ).start()


def translate_name_data(objects_list: list[Model], model: Model):
    objects_names_list = []
    try:
        translated = translator.translate_batch(
            [obj.name for obj in objects_list]
        )
        for obj, translated_name in zip(objects_list, translated):
            obj.name_en = translated_name,
            objects_names_list.append(obj)

        model.objects.bulk_update(objects_names_list, ['name_en'])
    except Exception as error:
        print(f'{obj.title} {error}')


