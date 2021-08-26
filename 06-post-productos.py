# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization

domain = []

limit = 4000

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]

# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]


sync_model(db1, db2, 'product.attribute.value', ['id', 'html_color', 'name', 'sequence'], ['is_custom'], ['attribute_id'], [], domain, offset=offset, limit=limit)

dont_sync = []
for attribute in db1.env['product.attribute'].search([]):
  error_lines = db1.env['product.template.attribute.line'].search([('attribute_id', '=', attribute.id), ('value_ids.attribute_id', '!=', attribute.id)])
  dont_sync += error_lines.ids
sync_model(db1, db2, 'product.template.attribute.line', ['id'], [], ['product_tmpl_id', 'attribute_id'], ['value_ids'], domain + [('id', 'not in', dont_sync)], offset=offset, limit=limit)

from_v12 = '12.0' in db1.db.server_version()
to_v12 = '12.0' in db2.db.server_version()
# solo sincronizamos este modelo de v12 a v12, en v13 se crea solo (el cambio fue acá https://github.com/odoo/odoo/commit/296c2ea13d206a10adb868b143120896d46e3519)
if from_v12 and to_v12:
  # de v12 a v12 va el product_tmpl_id
  sync_model(db1, db2, 'product.template.attribute.value', ['id', 'price_extra', 'html_color',], ['is_custom'], ['product_attribute_value_id', 'product_tmpl_id',], [], domain, offset=offset, limit=limit)

sync_model(db1, db2, 'product.template.attribute.exclusion', ['id',], [], ['product_template_attribute_value_id', 'product_tmpl_id',], ['value_ids'], domain, offset=offset, limit=limit)

# esto no porque es data de la sale order
# sync_model(db1, db2, 'product.attribute.custom.value', ['id', 'custom_value'], [], ['attribute_value_id', 'sale_order_line_id'], [], domain)
diff --git a/02-pre-productos.py b/02-pre-productos.py
