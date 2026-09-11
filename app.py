from flask import Flask, render_template, abort
import os

app = Flask(__name__)

# =========================================================
# IMAGE FOLDERS
# =========================================================

IMAGE_PATH = os.path.join(app.static_folder, "images")

FOLDERS = [
    {
        "folder": "3D Stage Concepts",
        "title": "3D STAGE CONCEPTS",
        "description": "Our professional 3D stage concepts and event designs."
    },
    {
        "folder": "Indoor and Outdoor stage designs",
        "title": "INDOOR & OUTDOOR STAGE DESIGNS",
        "description": "Stage designs created for indoor and outdoor events."
    },
    {
        "folder": "LED Screens & Lighting Productions",
        "title": "LED SCREENS & LIGHTING PRODUCTIONS",
        "description": "LED screens, lighting setups and production work."
    },
    {
        "folder": "Live Streaming",
        "title": "LIVE STREAMING",
        "description": "Live streaming and broadcast production projects."
    },
    {
        "folder": "Sound & Backline Productions",
        "title": "SOUND & BACKLINE PRODUCTIONS",
        "description": "Professional sound systems, backline and live production."
    }
]


# =========================================================
# GET IMAGES FROM A FOLDER
# =========================================================

def get_images(folder_name):
    folder_path = os.path.join(IMAGE_PATH, folder_name)

    if not os.path.exists(folder_path):
        return []

    images = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp", ".gif")
        ):
            images.append(filename)

    images.sort()

    return images


# =========================================================
# BUILD CATALOG
# =========================================================

def get_catalog():
    catalog = []

    for item in FOLDERS:
        images = get_images(item["folder"])
        cover = None

        if images:
            cover = images[0]

        catalog.append({
            "folder": item["folder"],
            "title": item["title"],
            "description": item["description"],
            "images": images,
            "count": len(images),
            "cover": cover
        })

    return catalog


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    catalog = get_catalog()

    return render_template(
        "index.html",
        folders=catalog,
        catalog=catalog
    )


# =========================================================
# GALLERY PAGE
# =========================================================

@app.route("/gallery/<path:folder>")
def gallery(folder):
    selected = None

    for item in FOLDERS:
        if item["folder"] == folder:
            selected = item
            break

    if selected is None:
        abort(404)

    images = get_images(folder)

    return render_template(
        "gallery.html",
        folder=folder,
        title=selected["title"],
        description=selected["description"],
        images=images
    )


# =========================================================
# SECOND GALLERY ROUTE
# =========================================================

@app.route("/gallery_folder/<path:folder>")
def gallery_folder(folder):
    selected = None

    for item in FOLDERS:
        if item["folder"] == folder:
            selected = item
            break

    if selected is None:
        abort(404)

    images = get_images(folder)

    return render_template(
        "gallery_folder.html",
        folder=folder,
        title=selected["title"],
        description=selected["description"],
        images=images
    )


# =========================================================
# BOOKING PAGE
# =========================================================

@app.route("/booking")
def booking():
    return render_template("booking.html")


# =========================================================
# RUN WEBSITE
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
