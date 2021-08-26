# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization
# Modificacion GabrielT 2020-07-04 Se incluyo: description_website
# Modificacion GabrielT 2020-08-07 Se incluyo: uom_po_id
# Modificacion GabrielT 2020-11-16 Se incluyo: 'list_price_type','sale_margin'

domain = []

limit = 1500

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]
  #domain = [('write_date', '>', '2020-12-14')]
# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]

# problemaPhoenix = True
# if problemaPhoenix:
#   domain += [('default_code', 'not like', 'PHO')]
  

# # NOTA por ahora el campo active no lo llevamos, si lo incorporamos en product.template tal vez debamos mejorar algo de performance en el "write" de pt que hace writes a los pp
# y no haria falta total los pp los escribimos nosotros luego
# hablamos con manu de por ahora tratar de zafar
# IMPORTANTE además sospecho que el campo active hizo que se dupliquen algunas variantes
# IMPORTANTE: se sincroniza el primer impuesto disponible a una sola cia (la primera en la cual se instaló el plan de cuentas) para el resto de las compañías se sincroniza el impuesto con un cron de neored personalization
sync_model(db1, db2, 'product.template',
  ['id', 'name', 'warranty', 'type', 'description', 'description_sale', 'description_purchase',
  'neored_image_url', 
  # 'image', 
  # product manufacturer
  'manufacturer_pname', 'manufacturer_pref', 'manufacturer_purl',
  # ecommerce
  'inventory_availability',
  'available_threshold', 'custom_message',
  'description_website',
  # planned price (Al final manu dijo de no llevarlo)
  # 'list_price_type', 'computed_list_price_manual', 'sale_margin', 'sale_surcharge', 'other_currency_list_price', 'list_price',
  # replenishment fields
  'list_price_type','sale_margin',
  'replenishment_cost_last_update', 'replenishment_base_cost', 'replenishment_cost_type',
  # # inventory tab
  'sale_delay', 'hs_code', 'description_pickingout', 'description_pickingin',
  # # website seo
  'website_meta_title', 'website_meta_description', 'website_meta_keywords', 'website_meta_og_img',
  ],
  [
    'purchase_ok', 'sale_ok',
  ],
  [
    'categ_id', 'replenishment_cost_rule_id', 'product_brand_id', 'other_currency_id', 'replenishment_base_cost_currency_id', 'product_attribute_template_id',
    'manufacturer',
    'uom_id',
    'product_abstract_id', 'uom_po_id',
  ],
  [
    'public_categ_ids', 'optional_product_ids', 'alternative_product_ids', 'accessory_product_ids',
    'taxes_id', 'supplier_taxes_id',
  ], domain, offset=offset, limit=limit)

