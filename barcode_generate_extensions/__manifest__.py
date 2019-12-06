
{
    'name': 'Generate Barcodes Extensions',
    'summary': 'Generate Barcodes for Multi Models',
    'version': '12.0.1.0.1',
    'category': 'Tools',
    'author':'OnurUgur,Codequarters',
    'website': 'https://www.codequarters.com',
    'license': 'AGPL-3',
    'depends': [
        'barcodes','barcodes_generator_abstract','barcodes_generator_product','product'
    ],
    'data': [
        'views/product_views.xml',
    ],
    'demo': [
    ],
    'external_dependencies': {'python': ['barcode']},
}
