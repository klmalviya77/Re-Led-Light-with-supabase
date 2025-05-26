from app import db
from datetime import datetime
import json

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    specifications = db.Column(db.Text)  # JSON string for specs
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_specifications(self):
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except:
                return {}
        return {}

    def set_specifications(self, specs_dict):
        self.specifications = json.dumps(specs_dict)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(20), default='')
    customer_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

class Catalogue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    pdf_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    featured = db.Column(db.Boolean, default=False)

def init_sample_data():
    """Initialize the database with sample LED lighting products"""

    # Create categories
    categories = [
        Category(name="Indoor LED Lights", description="High-quality LED lights for indoor spaces"),
        Category(name="Outdoor LED Lights", description="Weather-resistant LED lighting solutions"),
        Category(name="Smart LED Lights", description="Wi-Fi enabled smart lighting systems"),
        Category(name="Commercial LED Lights", description="Professional LED lighting for businesses"),
        Category(name="Decorative LED Lights", description="Artistic and decorative LED lighting")
    ]

    for category in categories:
        db.session.add(category)

    db.session.commit()

    # Stock photo URLs for LED products
    led_images = [
        "https://pixabay.com/get/g9c3cc6bb05affe8e153cb913d577828207e78c474e41ffb1a257546cbfeaf1418f87371177b508a037ba4dd8a7119b684818ad50599bca1cfbb096a94d5ee0a0_1280.jpg",
        "https://pixabay.com/get/gdbd5df027b3c22dc2a0062bed546d56aa10b4868deed4cbb151e810c3a208ccc486d69685afe1ee58a6190d5dc4a64c8bc4f24e7c8511653be4be2983217a8c3_1280.jpg",
        "https://pixabay.com/get/g2d7c3185fbeb039b68f8137b8424870b4b59c4cb1c5629a9cc500009b72c7de5533e7da973627fd761b5ae7d9f1754d9586b9a3a6d4242a05ce733cf7db03326_1280.jpg",
        "https://pixabay.com/get/g1b65e174a63089ae28753cafeb81932514f8a9bf40f5e0dd1a5042314c93a3690c2e1848b87af3cd751899d53fc4f43ada9742665967669b4afc37c323750da0_1280.jpg",
        "https://pixabay.com/get/g8abd9b49ddbb96f9a3105669f569f1209124b4cf7d557b568fb1d623e397ba1950a92c2de45366d611ea95174c6d7fca6c343a6ea1e3467c20f33e4daac961e7_1280.jpg",
        "https://pixabay.com/get/gb020c7483795719a46214a1ecd946bfc14b01927df031ae4db4c49429dfb83c586c7c3e669920ae798a838acee958e9bd854c2ad477b7d53250740f0a736d285_1280.jpg",
        "https://pixabay.com/get/g0b95f0cc0b3cb2c65f55a197eb31c625d68f0fe995603ac141b10d6fee8eb9a5470e8b2db360c612ad0dfb32f9905efc844ea3c30379b01b6dc4d5a489bc60dc_1280.jpg",
        "https://pixabay.com/get/g13553095412d068b7b79aaaf865b190ff18bb5dbdd4a1729634bc693019e596647f3de0e1f87da0649638f3bc6286ada0c6c4eaa4eaf596c84c29b66952c674b_1280.jpg"
    ]

    fixture_images = [
        "https://pixabay.com/get/g546fa313ebdd3efe2b380fb63ad0a2797d874da516c54aef62b3260110bee9e44aaae8dd8fd1f1709ec4f61b7975f68fa505a6ae2735c900b72b6c9fbab61eff_1280.jpg",
        "https://pixabay.com/get/g947559e7c54c810b9ce2b5bf26e4c891a811bfa97c902ec2cd46a297e72cb8b5977d1af4c9b0e26293477947575c09580b50ed109a91bab004da5602c8f754c0_1280.jpg",
        "https://pixabay.com/get/gbe46e330f736def9de33670bd8c02cc9959f5da5f5f5ebd71c3bc427d4afed0a16dc1551c524508fc7c724143990861d82d97a6c5b0b2ec3beef044c15003e7a_1280.jpg",
        "https://pixabay.com/get/gf1e502576bcb071a5ca5b7a6c885e622340a2fe335f3e674021f72bf201de22aca60210cb52ff4896aa87f450f5129b4bf7215628ed76b57caeb62e0b9cd8f69_1280.jpg"
    ]

    interior_images = [
        "https://pixabay.com/get/g519a7f540df7fecca5d5d2003e3a56ea370648c1fd2d5d4829ddf049fdbc8a85d2e4cf8a4b91cbdf384ea42d0683f0685960d8fcc8a488ca019322756458a55c_1280.jpg",
        "https://pixabay.com/get/g701b898667bfe5d103c65f4236c7155e0059ad0bba2aca333a02896e2d7b9efa4d7dbd7a8fdfde1d6bb39e230bc09b49447b3eff1dd18f8c216f9573e677b0b4_1280.jpg",
        "https://pixabay.com/get/g5237c677fb61678715ee000000daa108cfdf67aca86c0b9f5942dc05d927e8b736e3c047c9d5af942bf90048e89125f66bc617de22f883c3fe6a474e0f6dfc66_1280.jpg",
        "https://pixabay.com/get/g1688ce62e67fae03b405e02dd14f6ef9a7d9f7faf4c0d55d5df312e59d543b62d4de53d6e171a27212d660a3c9ae79a43cb2a63194cb7c0206375668a68434c7_1280.jpg"
    ]

    # Create sample products
    products = [
        # Indoor LED Lights
        Product(name="Premium LED Strip Light 5M", description="High-quality RGB LED strip with remote control. Perfect for accent lighting and mood creation.", 
                price=29.99, stock=50, image_url=led_images[0], category_id=1, featured=True,
                specifications='{"Power": "12W", "Length": "5 meters", "Color": "RGB", "Waterproof": "IP65", "Voltage": "12V DC"}'),

        Product(name="Smart LED Bulb E27 9W", description="Wi-Fi enabled smart bulb with color changing capabilities and app control.", 
                price=19.99, stock=75, image_url=led_images[1], category_id=3, featured=True,
                specifications='{"Power": "9W", "Base": "E27", "Lumens": "800lm", "Color Temperature": "2700K-6500K", "Smart Features": "Wi-Fi, App Control"}'),

        Product(name="LED Panel Light 60x60cm", description="Professional ceiling panel light with even light distribution for offices and homes.", 
                price=89.99, stock=30, image_url=led_images[2], category_id=4,
                specifications='{"Power": "40W", "Size": "60x60cm", "Lumens": "4000lm", "Color Temperature": "4000K", "Mounting": "Ceiling"}'),

        Product(name="Flexible LED Tape 3528", description="High-density LED tape for continuous lighting applications.", 
                price=15.99, stock=100, image_url=led_images[3], category_id=1,
                specifications='{"Power": "4.8W/m", "LEDs": "120/m", "Color": "Warm White", "Voltage": "12V DC", "CRI": ">80"}'),

        # Outdoor LED Lights
        Product(name="Waterproof LED Floodlight 50W", description="Heavy-duty outdoor floodlight with IP66 rating for all weather conditions.", 
                price=45.99, stock=40, image_url=led_images[4], category_id=2, featured=True,
                specifications='{"Power": "50W", "Lumens": "5000lm", "IP Rating": "IP66", "Beam Angle": "120°", "Voltage": "AC 85-265V"}'),

        Product(name="Solar LED Garden Light", description="Eco-friendly solar-powered garden light with automatic dusk-to-dawn operation.", 
                price=34.99, stock=60, image_url=led_images[5], category_id=2,
                specifications='{"Power": "5W", "Solar Panel": "6V 2W", "Battery": "3.7V 2200mAh", "Working Time": "8-10 hours", "IP Rating": "IP65"}'),

        # Modern Fixtures
        Product(name="Modern LED Pendant Light", description="Sleek pendant light fixture perfect for dining rooms and kitchen islands.", 
                price=129.99, stock=25, image_url=fixture_images[0], category_id=5, featured=True,
                specifications='{"Power": "24W", "Material": "Aluminum + Acrylic", "Color Temperature": "3000K", "Dimmable": "Yes", "Suspension": "Adjustable"}'),

        Product(name="Contemporary LED Chandelier", description="Elegant multi-tier LED chandelier for modern living spaces.", 
                price=299.99, stock=15, image_url=fixture_images[1], category_id=5,
                specifications='{"Power": "60W", "Material": "Crystal + Metal", "Diameter": "80cm", "Height": "60cm", "Dimmable": "Yes"}'),

        Product(name="Minimalist LED Wall Sconce", description="Clean-lined wall sconce providing ambient lighting for hallways and bedrooms.", 
                price=79.99, stock=35, image_url=fixture_images[2], category_id=1,
                specifications='{"Power": "12W", "Material": "Brushed Aluminum", "Dimensions": "30x15x8cm", "IP Rating": "IP44", "Beam Direction": "Up/Down"}'),

        Product(name="LED Track Lighting System", description="Adjustable track lighting system perfect for galleries and retail spaces.", 
                price=189.99, stock=20, image_url=fixture_images[3], category_id=4,
                specifications='{"Power": "3x15W", "Track Length": "1.5m", "Heads": "3 adjustable", "Beam Angle": "30°", "Color Temperature": "4000K"}'),

        # Interior Lighting
        Product(name="LED Recessed Downlight 7W", description="Slim profile recessed downlight for seamless ceiling integration.", 
                price=24.99, stock=80, image_url=interior_images[0], category_id=1,
                specifications='{"Power": "7W", "Cutout": "85mm", "Depth": "25mm", "Lumens": "700lm", "Color Temperature": "3000K"}'),

        Product(name="Smart LED Strip Controller", description="Advanced controller for RGB LED strips with music sync and app control.", 
                price=39.99, stock=45, image_url=interior_images[1], category_id=3,
                specifications='{"Channels": "4 (RGB+W)", "Max Load": "288W", "Control": "Wi-Fi + Bluetooth", "Features": "Music Sync, Timer, DIY Mode"}'),

        Product(name="LED Under Cabinet Light", description="Low-profile under cabinet lighting for kitchen and workspace illumination.", 
                price=18.99, stock=90, image_url=interior_images[2], category_id=1,
                specifications='{"Power": "8W", "Length": "30cm", "Color Temperature": "4000K", "Mounting": "Magnetic", "Sensor": "Motion + Touch"}'),

        Product(name="Decorative LED String Lights", description="Warm white decorative string lights perfect for parties and ambiance.", 
                price=12.99, stock=120, image_url=interior_images[3], category_id=5,
                specifications='{"Power": "6W", "Length": "10m", "LEDs": "100", "Color": "Warm White", "Modes": "8 different patterns"}'),
    ]

    for product in products:
        db.session.add(product)

    db.session.commit()

    # Add sample catalogues
    catalogues = [
        Catalogue(
            title="LED Indoor Lighting Catalogue 2024",
            description="Complete range of indoor LED lighting solutions including bulbs, panels, and decorative lights.",
            pdf_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            thumbnail_url="https://via.placeholder.com/300x400/0d6efd/ffffff?text=Indoor+LED+Catalogue",
            category="Indoor Lighting",
            featured=True
        ),
        Catalogue(
            title="Outdoor LED Solutions",
            description="Weather-resistant outdoor lighting including floodlights, garden lights, and street lighting.",
            pdf_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            thumbnail_url="https://via.placeholder.com/300x400/198754/ffffff?text=Outdoor+LED+Catalogue",
            category="Outdoor Lighting"
        ),
        Catalogue(
            title="Smart LED Technology Guide",
            description="Advanced smart lighting systems with Wi-Fi connectivity and app control features.",
            pdf_url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            thumbnail_url="https://via.placeholder.com/300x400/0dcaf0/ffffff?text=Smart+LED+Guide",
            category="Smart Lighting",
            featured=True
        )
    ]

    for catalogue in catalogues:
        db.session.add(catalogue)

    db.session.commit()
    print("Sample data initialized successfully!")