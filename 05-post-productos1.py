# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization

domain = []

limit = 20000

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]

# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]
  


sync_model(db1, db2, 'product.uoms', ['id', 'sequence'], ['sale_ok', 'purchase_ok'], ['uom_id', 'product_tmpl_id'], [], domain, offset=offset, limit=limit)

sync_model(db1, db2, 'product.template.tag', ['id', 'name', 'color'], [], [], ['product_tmpl_ids'], domain, offset=offset, limit=limit)

# en v13 el name empezó a ser obligatorio
if '12.0' in db2.db.server_version():
  sync_model(db1, db2, 'product.image', ['id', 'name', 'neored_image_url'], [], ['product_tmpl_id'], [], domain, offset=offset, limit=limit)
else:
  sync_model(db1, db2, 'product.image', ['id', 'name', 'neored_image_url'], [], ['product_tmpl_id'], [], domain + [('name', '!=', False)], offset=offset, limit=limit)


sync_model(
  db1, db2, 'product.supplierinfo',
  ['id', 'sequence', 'price', 'min_qty', 'delay', 'product_code', 'product_code_2', 'sequence', 'date_start', 'date_end'], [],
  ['name', 'product_id', 'product_tmpl_id', 'product_uom', 'replenishment_cost_rule_id', 'currency_id',], [], domain, offset=offset, limit=limit)
