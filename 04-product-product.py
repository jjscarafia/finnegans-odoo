# IMPORTANTE: si se hacen cambios se deben actualizar las acciones automáticas que protegen registros en neored_personalization

domain = []

limit = 5000

if last_cron_execution:
  domain = [('write_date', '>', last_cron_execution.strftime("%Y-%m-%d %H:%M:%S"))]
  #domain = [('write_date', '>', '2020-12-14')]
# desde que se empezo la sincronizacion se pueden haber creado, por ejemplo, product.tempalte, pero que no los hemos sincronizado y entonces daria error aca
# por eso solo sincronizamos hasta esta fecha, cualquier creación posterior se sincronizara en la proxima corrida
if last_sync_start:
  domain += [('write_date', '<=', last_sync_start.strftime("%Y-%m-%d %H:%M:%S"))]

# problemaPhoenix = True
# if problemaPhoenix:
#   domain += [('product_tmpl_id.default_code', 'not like', 'PHO')]

#problemaJunin = True
#if problemaJunin:
#   domain += [('product_tmpl_id.default_code', '!=', 'ARGAC24')]
#   domain += [('product_tmpl_id.default_code', '!=', 'FIS613558')]
#   domain += [('product_tmpl_id.default_code', 'not like', 'VEF')]
#   domain += [('product_tmpl_id.default_code', 'not like', 'FIS')]
#   domain += [('product_tmpl_id.default_code', 'not like', 'LUM')]


#problemaAbelcar = True
#if problemaAbelcar:
#   domain += [('product_tmpl_id.default_code', 'not like', 'PIN')]


# por ahora no estamos llevando el campo active, si lo incorporamos acá no haria falta mejorar performance, va bien
sync_model(db1, db2, 'product.product',
[
  'id', 'default_code', 'barcode',
  'weight', 'volume', 'product_length', 'product_height', 'product_width',
],
[
],
[
  'product_tmpl_id', 'dimensional_uom_id',
],
[],
domain, offset=offset, limit=limit)
