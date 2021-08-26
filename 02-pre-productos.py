# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization
# Gabriel Tiburtini : agregao sequence a product.replenishment_cost.rule.item

domain = []

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]

# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]

sync_model(db1, db2, 'product.category', ['id', 'name'], [], ['parent_id'], [], domain, 'parent_path')

sync_model(db1, db2, 'product.public.category',
['id', 'name', 'sequence', 'website_meta_title', 'website_meta_description', 'website_meta_keywords', 'website_meta_og_img',],
[],
['parent_id'], [], domain, 'parent_path')

# de v12 a v13 el type "time" cambió a "working_time", si estamos sincronizando de v12 a v13 no llevamos este campo y listo
if '13.0' in db2.db.server_version() and '12.0' in db1.db.server_version():
  uom_categ_fields = ['id', 'name',]
else:
  uom_categ_fields = ['id', 'name', 'measure_type']
sync_model(db1, db2, 'uom.category', uom_categ_fields, [], [], [], domain)

sync_model(db1, db2, 'uom.uom', ['id', 'name', 'uom_type', 'factor_inv', 'rounding', 'afip_code', 'arba_code'], ['active'], ['category_id'], [], domain)

# IMPORTANTE por ahora no usamos porque esta mal, estamos viendo las modificaciones en db2 mientras deberíamos chequear si se modificaron en db1, pero luego los ids no sol necesariamente los mismos
# en el ticket # 33983 le escribimos a gabriel preguntando por un workaround de bloquear borrado de reglas
# borramos las lineas de reglas de costo que se sincronizan (las que no terminan con _L) porque podría haberse borrado alguna regla en catalogo y el borrado no se sincroniza
# esto es bastante lento porque ahora el campo price_net es almacenado, entonces, al borrar las lineas se recomputan todos los price net y luego se vuelve a re computar cuando se crean
# distributor_ids = db2.env['product.replenishment_cost.rule'].search([('name', '=like', '%\_L')]).ids
# modified_not_distributor_ids = db2.env['product.replenishment_cost.rule'].search(domain + [('id', 'not in', distributor_ids)]).ids
# db2.env['product.replenishment_cost.rule.item'].with_context(odumbo_sync=True).search([('replenishment_cost_rule_id', 'in', modified_not_distributor_ids)]).unlink()

sync_model(db1, db2, 'product.replenishment_cost.rule', ['id', 'name'], [], [], [], domain)

sync_model(db1, db2, 'product.replenishment_cost.rule.item', ['id', 'name', 'percentage_amount', 'fixed_amount','sequence'], [], ['replenishment_cost_rule_id'], [], domain)
# distributor_ids = db1.env['product.replenishment_cost.rule'].search([('name', '=like', '%\_L')]).ids
# modified_not_distributor_ids = db1.env['product.replenishment_cost.rule'].search(domain + [('id', 'not in', distributor_ids)]).ids
# sync_model(db1, db2, 'product.replenishment_cost.rule.item', ['id', 'name', 'percentage_amount', 'fixed_amount'], [], ['replenishment_cost_rule_id'], [], domain + [('id', 'not in', distributor_ids)])

sync_model(db1, db2, 'product.brand', ['id', 'name', 'description', 'logo'], [], ['partner_id'], [], domain)

sync_model(db1, db2, 'product.attribute.template', ['id', 'name'], [], [], [], domain)

sync_model(db1, db2, 'product.attribute', ['id', 'name', 'sequence', 'create_variant'], [], [], [], domain)

sync_model(db1, db2, 'product.abstract', ['id'], [], [], [], domain)

# solo para que les agregue el ID de odumbo
sync_model(db1, db2, 'res.currency', ['id'], [], [], [], domain)

# dummy sync de taxes para setearles el external id, al proposito no pasamos type ni nada porque queremos que de error si no existe ya que no deberiamos crear ninguno
if '12.0' in db1.db.server_version():
  # v12
  sync_model(db1, db2, 'account.tax', ['id'], [], [], [], domain + [('tax_group_id.tax', '=', 'vat'), ('tax_group_id.type', '=', 'tax')])
else:
  # v13+
  sync_model(db1, db2, 'account.tax', ['id'], [], [], [], domain + [('tax_group_id.l10n_ar_vat_afip_code', '!=', False)])

diff --git a/03-product-template.py b/03-product-template.py
