# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization

# IMPORTANTE: sincronización entre distintas versiones:
# para futuras sincronizaciones entre distintas versiones ver de agregar campo related en version anterior ya que el write de campos related se hace en distintos pasos y es menos performante y pueda dar errores de constraints

domain = []

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]

# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]

# obtenemos todos los partners con identificación en catalogo
db1_id_numbers_read = db1.env["res.partner"].search_read(domain + [('main_id_number', '!=', False)], ['main_id_number'])
db1_id_numbers_read = {x['main_id_number']:x['id'] for x in db1_id_numbers_read}

# buscamos todos los partners ids que ya fueron sincronizados con odumbo
db2_odumbo_ids = db2.env["ir.model.data"].search([("module", "=", '__odumbo__'), ("model", "=", 'res.partner')]).mapped('res_id')

# buscamos si existen partners que No fueron sincronizados y que tienen identiificación repetida en catalogo
db2_id_numbers_read = db2.env["res.partner"].search_read([('main_id_number', 'in', list(db1_id_numbers_read.keys())), ('id', 'not in', db2_odumbo_ids)], ['main_id_number'])

# creamos identificadores d odumbo para estos partners que ya existen en bd destino
for partner_read in db2_id_numbers_read:
  outcome = db2.env["ir.model.data"].load(["name", "model", "module", "res_id"], [["res_partner_%s" % db1_id_numbers_read[partner_read['main_id_number']], 'res.partner', '__odumbo__', partner_read['id']]])
  # raise Warning([["res_partner_%s" % db1_id_numbers_read[partner_read['main_id_number']], 'res.partner', '__odumbo__', partner_read['id']]])

from_v12 = '12.0' in db1.db.server_version()
to_v12 = '12.0' in db2.db.server_version()

# dummy syncpara setearles el external id, al proposito no pasamos type ni nada porque queremos que de error si no existe ya que no deberiamos crear ninguno
if from_v12 and to_v12:
  # de v12 a v12
  sync_model(db1, db2, 'afip.responsability.type', ['id'], [], [], [], domain)
  sync_model(db1, db2, 'res.partner.id_category', ['id'], [], [], [], domain)
elif from_v12:
  # de v12 a v13+
  sync_model(db1, db2, 'afip.responsability.type', ['id'], [], [], [], domain, target_model_name='l10n_ar.afip.responsibility.type')
  sync_model(db1, db2, 'res.partner.id_category', ['id'], [], [], [], domain, target_model_name='l10n_latam.identification.type')
else:
  # de v13+ a v13+
  sync_model(db1, db2, 'l10n_ar.afip.responsibility.', ['id'], [], [], [], domain)
  sync_model(db1, db2, 'l10n_latam.identification.type', ['id'], [], [], [], domain)

# al final pidieron llevar todo lo que sea proveedor mas todo el que este vinculado a un producto
supplier_ids = db1.env["product.supplierinfo"].search([]).mapped("name").ids
brand_partner_ids = db1.env["product.brand"].search([]).mapped("partner_id").ids
manufacturer_ids = db1.env["product.template"].search([('manufacturer', '!=', False)]).mapped("manufacturer").ids

sync_model(db1, db2, 'res.partner',
[
  'id', 'name', 'street', 'street2', 'city', 'zip', 'main_id_number'
  #'id', 'name', 'street', 'street2', 'city', 'zip', 'vat'
],
['active', 'customer', 'supplier', 'is_company',] if to_v12 else ['active', 'is_company',],
['afip_responsability_type_id', 'main_id_category_id',],
# ['l10n_ar_afip_responsibility_type_id', 'l10n_latam_identification_type_id',],
[],
domain + ['|', ('supplier', '=', True), ('id', 'in', supplier_ids + brand_partner_ids + manufacturer_ids)]) # ALWAYS BRING ALL PARTNERS, they might not be necessarily updated, and still be required by a product.
