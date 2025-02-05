CONFIG = {
    "BASE_URL": 'https://dentalstall.com/shop/page/{}/',
    "HEADERS": {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    },
    "SELECTORS": {
        "product_title": {'tag': 'h1', 'class': 'product_title'},
        "product_image": {'tag': 'div', 'class': 'woocommerce-product-gallery__image'},
        "product_list": {'tag': 'li', 'class': 'product'},
        "product_link": {'tag': 'h2', 'class': 'woo-loop-product__title'},
        "price": {'tag': 'span', 'class': 'woocommerce-Price-amount'},
    }
}
