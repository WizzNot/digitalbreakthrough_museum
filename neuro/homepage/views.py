from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import uuid
from tensorflow.keras.preprocessing import image
import numpy as np
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img, dtype=np.uint8)
    img = preprocess_input(img)
    return img


def home(request):
    template = "homepage/home.html"
    return render(request, template_name=template)


def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        context = {}
        image_file = request.FILES['image']
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image_file.name)[-1]
        fs = FileSystemStorage()
        fs.save("images/" + unique_filename, image_file)
        image_np = preprocess_image("images/" + unique_filename)
        group_index = settings.MODEL.predict(np.expand_dims(image_np, axis=0))
        category_name = settings.GROUPS[np.argmax(group_index[0])]
        context["category"] = category_name

        target_image_features = settings.MODEL_MOBILENET.predict(np.expand_dims(image_np, axis=0)).flatten()
        sims = cosine_similarity([target_image_features], settings.FEATURE_VECTORS)[0]
        similarities = [(sims[i], i) for i in range(len(sims))]
        most_similar_index = sorted(similarities, key=lambda z: z[0], reverse=True)[:10]
        most_similar_index = [settings.DF["id"].iat[i[1]] for i in most_similar_index]
        selected_object = settings.CSV_DF[settings.CSV_DF['object_id'] == int(most_similar_index[0])]
        if not selected_object.empty:
            name = selected_object['name'].values[0]
            img_name = selected_object['img_name'].values[0]
            context["most_similar_path"] = os.path.join("train", str(most_similar_index[0]), img_name)
            context["most_similar_name"] = name
        else:
            raise f"{most_similar_index[0]} not in object id's"
        items = []
        for i in most_similar_index[1:]:
            selected_object = settings.CSV_DF[settings.CSV_DF['object_id'] == int(i)]
            if not selected_object.empty:
                obj = {"name": selected_object["name"].values[0], "path": os.path.join("train", str(i), selected_object['img_name'].values[0])}
                items.append(obj)
            else:
                raise f"{i} not in object id's"
        context["items"] = items
        return render(request, 'homepage/upload_success.html', context)
    return render(request, 'homepage/upload_fail.html')