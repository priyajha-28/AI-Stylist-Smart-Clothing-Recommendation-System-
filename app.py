from flask import Flask, render_template, request, url_for, redirect
from PIL import Image, ImageOps
import os
import random
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# ---------- Helpers ----------
def simulate_body_shape_detection(image_path):
    # Demo/stub: always returns Hourglass for now
    return 'Hourglass'


def infer_description_from_filename(overlay_relpath):
    try:
        base = os.path.basename(overlay_relpath)
        name = os.path.splitext(base)[0]
        parts = re.sub(r'[^0-9a-zA-Z]+', '_', name).lower().split('_')
        event_tokens = {
            'brunch': 'Casual daytime outfit — breathable fabrics and a relaxed fit.',
            'cocktail': 'Cocktail outfit — dressy, knee- to midi-length, evening-ready.',
            'wedding': 'Formal wedding outfit — floor-length or dressy formalwear.',
            'office': 'Professional office attire — tailored pieces and clean lines.',
            'concert': 'Edgy concert outfit — statement top and relaxed bottoms.'
        }
        for p in parts:
            if p in event_tokens:
                return event_tokens[p]
        pretty = " ".join([p for p in parts if p not in ('hg', '')]).strip()
        pretty = pretty.replace('-', ' ')
        if pretty:
            return pretty.title() + " outfit — a stylish choice."
        return "Stylish outfit — a great option for the selected event."
    except Exception:
        return "Stylish outfit — a great option for the selected event."


def composite_overlay_on_white(overlay_relpath):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    overlay_path = os.path.join(static_dir, overlay_relpath)
    if not os.path.exists(overlay_path):
        return url_for('static', filename='overlays/default_overlay.png')
    try:
        overlay = Image.open(overlay_path).convert("RGBA")
    except Exception:
        return url_for('static', filename='overlays/default_overlay.png')

    w, h = overlay.size
    canvas_w = max(w, 800)
    canvas_h = max(h, 1000)
    white_bg = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 255))
    overlay_resized = ImageOps.contain(overlay, (canvas_w, canvas_h))
    px = (canvas_w - overlay_resized.size[0]) // 2
    py = (canvas_h - overlay_resized.size[1]) // 2
    white_bg.alpha_composite(overlay_resized, dest=(px, py))

    uploads_dir = os.path.join(static_dir, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    out_name = f"overlay_preview_{random.randint(1000,9999)}.jpg"
    out_path = os.path.join(uploads_dir, out_name)
    white_bg.convert("RGB").save(out_path, format='JPEG', quality=90)
    return url_for('static', filename='uploads/' + out_name)


def composite_overlay_on_user(user_img_path, overlay_relpath, scale_factor=1.0, y_offset=0):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    overlay_path = os.path.join(static_dir, overlay_relpath)

    if not os.path.exists(user_img_path):
        print("Missing user image:", user_img_path)
        return url_for('static', filename=overlay_relpath)
    if not os.path.exists(overlay_path):
        print("Missing overlay:", overlay_path)
        return url_for('static', filename=overlay_relpath)

    try:
        user_img = Image.open(user_img_path).convert("RGBA")
    except Exception as e:
        print("Error opening user image:", e)
        return url_for('static', filename=overlay_relpath)

    try:
        overlay = Image.open(overlay_path).convert("RGBA")
    except Exception as e:
        print("Error opening overlay:", e)
        return url_for('static', filename=overlay_relpath)

    usr_w, usr_h = user_img.size
    # enforce at least 1px to avoid errors
    target_w = int(max(1, usr_w * float(scale_factor)))
    overlay_resized = ImageOps.contain(overlay, (target_w, usr_h))
    px = (usr_w - overlay_resized.size[0]) // 2
    py = (usr_h - overlay_resized.size[1]) // 2 + int(y_offset)

    composite = Image.new("RGBA", user_img.size)
    composite.paste(user_img, (0, 0))
    composite.alpha_composite(overlay_resized, dest=(px, py))

    uploads_dir = os.path.join(static_dir, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    out_name = f"user_vto_{random.randint(1000,9999)}.jpg"
    out_path = os.path.join(uploads_dir, out_name)
    composite.convert("RGB").save(out_path, format='JPEG', quality=90)
    return url_for('static', filename='uploads/' + out_name)


def normalize_name(fname):
    # normalizes filename (no extension) to only alnum and underscores, lowercase
    base = os.path.splitext(fname)[0]
    return re.sub(r'[^0-9a-zA-Z]+', '_', base).lower()


# ---------- Data: RECOMMENDATIONS (edit descriptions if you want exact phrasing) ----------
RECOMMENDATIONS = {
    ('Hourglass', 'Casual Brunch'): [
        {
            'name': 'Floral Wrap Midi Dress',
            'description': 'Casual daytime outfit — breathable fabrics and a relaxed fit.',
            'tip': 'A floral wrap brings soft definition to the waist and a breezy casual feel.',
            'sustainable_material': 'Organic Cotton or Tencel',
            'overlay_img_url': 'overlays/hg_brunch_1.png',
        },
    ],
    ('Hourglass', 'Cocktail Party'): [
        {
            'name': 'Black Spaghetti-Strap Quilted Midi',
            'description': 'Cocktail outfit — dressy, knee- to midi-length, evening-ready.',
            'tip': 'The fitted bodice and full midi skirt naturally complement your waist-to-hip curve.',
            'sustainable_material': 'Recycled Polyester Blend',
            'overlay_img_url': 'overlays/hg_cocktail_1.png',
        },
    ],
    ('Hourglass', 'Formal Wedding'): [
        {
            'name': 'Elegant Column Gown',
            'description': 'Formal wedding outfit — floor-length or dressy formalwear.',
            'tip': 'This style highlights your balanced proportions. Focus on a defined waistline!',
            'sustainable_material': 'Recycled Polyester or Tencel Luxe',
            'overlay_img_url': 'overlays/hg_wedding_1.png',
        },
    ],
    ('Default', 'Default'): [
        {
            'name': 'Classic Fit Dress',
            'description': 'Timeless, versatile dress suitable for many occasions.',
            'tip': 'Neutral silhouettes are safe and flattering for most shapes.',
            'sustainable_material': 'Recycled Fibers',
            'overlay_img_url': 'overlays/default_overlay.png',
        }
    ]
}

SEASONAL_PALETTES = {
    'Hourglass': ['#E6B8C0', '#C7EFCF', '#FFE3A9', '#D0E7FF'],
    'Default': ['#EFEFEF', '#D8D8D8', '#BFBFBF']
}


# ---------- Routes ----------
@app.route('/', methods=['GET'])
def index():
    events = [
        "Formal Wedding", "Cocktail Party", "Casual Brunch",
        "Office/Professional Meeting", "Music Festival/Concert"
    ]
    return render_template('login.html', events=events)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return redirect(url_for('index'))

    user_name = request.form.get('user_name', 'Client')
    user_email = request.form.get('user_email', 'N/A')
    user_password = ''
    events = ["Formal Wedding", "Cocktail Party", "Casual Brunch",
              "Office/Professional Meeting", "Music Festival/Concert"]
    return render_template('upload_photo.html',
                           user_name=user_name,
                           user_email=user_email,
                           user_password=user_password,
                           events=events)


@app.route('/recommend', methods=['POST'])
def recommend():
    file = request.files.get('user_photo')
    event_type = request.form.get('event_type', 'Casual Brunch')
    user_name = request.form.get('user_name', 'Client')
    user_email = request.form.get('user_email', 'N/A')

    if file is None:
        return "Error: No file uploaded", 400

    # 1) Save uploaded file
    filename = f"{random.randint(1000, 9999)}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        img = Image.open(file.stream)
        img.save(filepath)
    except Exception as e:
        print("File error during save:", e)
        return "Error: Please upload a valid image file.", 400

    # 2) Simulated detection
    detected_shape = simulate_body_shape_detection(filepath)

    # 3) Get recommendations for detected shape + event
    key = (detected_shape, event_type)
    recommendations_list = RECOMMENDATIONS.get(key, RECOMMENDATIONS.get(('Default', 'Default')))
    color_palette = SEASONAL_PALETTES.get(detected_shape, SEASONAL_PALETTES['Default'])
    if not color_palette:
        color_palette = SEASONAL_PALETTES.get('Default')

    # 4) gather overlays list from static/overlays for gallery and auto generation
    static_overlays_dir = os.path.join(os.path.dirname(__file__), 'static', 'overlays')
    try:
        all_overlays = sorted([f for f in os.listdir(static_overlays_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    except Exception:
        all_overlays = []

    # Map event labels to tokens (lowercase tokens used to match filenames)
    event_token_map = {
        'Casual Brunch': ['brunch'],
        'Cocktail Party': ['cocktail'],
        'Formal Wedding': ['wedding'],
        'Office/Professional Meeting': ['office'],
        'Music Festival/Concert': ['concert']
    }
    tokens = event_token_map.get(event_type, [])

    # per-overlay tuning map (normalized filenames without extension)
    per_overlay_positions = {
        # example entries (uncomment and edit to tune)
        # 'hg_brunch_1': {'scale': 0.95, 'y_offset': -40},
        # 'hg_cocktail_1': {'scale': 0.92, 'y_offset': -50},
    }

    # If recommendations_list is shorter than overlays, try to auto-generate filtered by event token
    if len(recommendations_list) < len(all_overlays):
        filtered_overlays = []
        for f in all_overlays:
            norm = normalize_name(f)
            if tokens:
                if any(tok in norm for tok in tokens):
                    filtered_overlays.append(f)
        # debug print
        print(f"[DEBUG] event_type='{event_type}', tokens={tokens}, matched overlays={filtered_overlays}")

        if filtered_overlays:
            auto_list = []
            for fname in filtered_overlays:
                rel = f"overlays/{fname}"
                auto_list.append({
                    'name': fname.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title(),
                    'description': infer_description_from_filename(rel),
                    'tip': 'Automatically generated option from overlay image.',
                    'sustainable_material': '',
                    'overlay_img_url': rel
                })
            recommendations_list = auto_list
        else:
            print(f"[DEBUG] No overlays matched event '{event_type}' — keeping RECOMMENDATIONS entries.")

    # 5) Build distinct VTO preview per outfit by compositing overlay on user photo
    final_vto_options = []
    for outfit in recommendations_list:
        overlay_rel = outfit.get('overlay_img_url', 'overlays/default_overlay.png')
        if not outfit.get('description'):
            outfit['description'] = infer_description_from_filename(overlay_rel)

        # determine per-overlay tuning if provided
        norm_key = normalize_name(os.path.basename(overlay_rel))
        tuning = per_overlay_positions.get(norm_key, None)
        if tuning:
            scale = tuning.get('scale', 1.0)
            y_off = tuning.get('y_offset', 0)
        else:
            scale = 1.0
            y_off = 0

        try:
            vto_output_url = composite_overlay_on_user(filepath, overlay_rel, scale_factor=scale, y_offset=y_off)
        except Exception as e:
            print("VTO composite error:", e)
            vto_output_url = composite_overlay_on_white(overlay_rel)

        vto_option = outfit.copy()
        vto_option['final_vto_url'] = vto_output_url
        final_vto_options.append(vto_option)

    # Arrange the best match first — pick the first item as the "perfect match"
    primary_option = final_vto_options[0] if final_vto_options else None
    other_options = final_vto_options[1:] if len(final_vto_options) > 1 else []

    events = [
        "Formal Wedding", "Cocktail Party", "Casual Brunch",
        "Office/Professional Meeting", "Music Festival/Concert"
    ]

    # ------------------ Filter overlays_list by selected event tokens ------------------
    filtered_overlays_list = []
    for f in all_overlays:
        norm = normalize_name(f)
        if tokens:
            if any(tok in norm for tok in tokens):
                filtered_overlays_list.append(f)

    # If nothing matched, fallback to ALL overlays (avoid empty gallery)
    if not filtered_overlays_list:
        filtered_overlays_list = all_overlays

    overlays_list = filtered_overlays_list
    # -----------------------------------------------------------------------------------------

    return render_template('index.html',
                           events=events,
                           primary_option=primary_option,
                           other_options=other_options,
                           detected_shape=detected_shape,
                           selected_event=event_type,
                           color_palette=color_palette,
                           user_name=user_name,
                           user_email=user_email,
                           overlays_list=overlays_list)


if __name__ == '__main__':
    app.run(debug=True)