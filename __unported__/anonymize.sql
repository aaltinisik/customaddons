UPDATE public.res_users
   SET active=False,
       password_crypt=NULL, password=NULL, google_calendar_token_validity=NULL,
       google_calendar_cal_id=NULL, google_calendar_rtoken=NULL, google_calendar_last_sync_date=NULL,
       google_calendar_token=NULL, context_map_website_id=NULL,
       context_route_map_website_id=NULL, oauth_access_token=NULL, oauth_uid=NULL,
       oauth_provider_id=NULL
WHERE
  res_users.login != 'admin';

  UPDATE public.res_users
   SET google_calendar_token_validity=NULL,
       google_calendar_cal_id=NULL, google_calendar_rtoken=NULL, google_calendar_last_sync_date=NULL,
       google_calendar_token=NULL, context_map_website_id=NULL,
       password_crypt='$pbkdf2-sha512$19000$MQYAYIwRQgghZKw1BqAUYg$cEqanQoFDYFSD5QnX6TQwK71IJLDaiS9fV6q2ta4gUmz9rzSpQr54jGINmV2xlyC3xejSMX7jbMcbnS5RPApFg',
       context_route_map_website_id=NULL, oauth_access_token=NULL, oauth_uid=NULL,
       oauth_provider_id=NULL
WHERE
  res_users.login = 'admin';

UPDATE public.ir_config_parameter
   SET  value=''
WHERE
  ir_config_parameter.key = 'google_redirect_uri' OR
  ir_config_parameter.key = 'google.geocode.key' OR
  ir_config_parameter.key = 'google_drive_client_id' OR
  ir_config_parameter.key = 'google_drive_client_secret' OR
  ir_config_parameter.key = 'google_calendar_client_secret' OR
  ir_config_parameter.key = 'google_calendar_client_id' OR
  ir_config_parameter.key = 'google_drive_authorization_code' OR
  ir_config_parameter.key = 'google_drive_refresh_token' OR
  ir_config_parameter.key = 'google_drive_client_id';

UPDATE ir_config_parameter SET  value='TEST' WHERE ir_config_parameter.key = 'ribbon.name';
UPDATE ir_config_parameter SET  value='rgba(240,0,0,.6)' WHERE ir_config_parameter.key = 'ribbon.background.color';

UPDATE ir_cron SET active=true
    WHERE
    ir_cron.model = 'res.users.login' or
    ir_cron.model = 'publisher_warranty.contract' or
    ir_cron.model = 'mail.thread' or
    ir_cron.model = 'sale.order' or
    ir_cron.model = 'currency.rate.update.service' or
    ir_cron.model = 'fetchmail.server' or
    ir_cron.model = 'mail.mail' or
    ir_cron.model = 'faxsend.queue' or
    ir_cron.model = 'printing.printer' or
    ir_cron.model = 'google.calendar';

UPDATE faxsend_account SET username='test', password = 'dummypass';

TRUNCATE faxsend_queue;

UPDATE public.res_company
   SET  pad_key='', pad_server='', hash_code='';

UPDATE public.fetchmail_server
   SET "user"='usr', password='pass',active=false;

UPDATE public.ir_mail_server
   SET smtp_user='usr', smtp_pass='pass';

UPDATE public.asterisk_server
   SET login='usr', password='pass', ip_address='';


ALTER TABLE public.product_product DROP CONSTRAINT IF EXISTS product_product_image_variant_attachment_id_fkey;
ALTER TABLE public.product_template DROP CONSTRAINT IF EXISTS product_template_image_attachment_id_fkey;
ALTER TABLE public.product_template DROP CONSTRAINT IF EXISTS product_template_image_medium_attachment_id_fkey;
ALTER TABLE public.product_template DROP CONSTRAINT IF EXISTS product_template_image_small_attachment_id_fkey;


TRUNCATE mail_followers,mail_mail_res_partner_rel,mail_compose_message_res_partner_rel,mail_compose_message_ir_attachments_rel,message_attachment_rel,mail_vote,mail_followers_mail_message_subtype_rel,
mail_message,mail_compose_message,mail_mail,mail_message_res_partner_rel,mail_notification;

TRUNCATE ir_attachment,email_template_attachment_rel,faxsend_queue,mail_compose_message_ir_attachments_rel,message_attachment_rel;



UPDATE public.product_product
   SET image_variant_attachment_id=null;

UPDATE public.product_template
   SET image_attachment_id=null,image_medium_attachment_id=null,image_small_attachment_id=null;

UPDATE public.hr_employee
   SET image=null, image_medium=null,
       image_small=null;


ALTER TABLE public.product_product
  ADD CONSTRAINT product_product_image_variant_attachment_id_fkey FOREIGN KEY (image_variant_attachment_id)
      REFERENCES public.ir_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL;

ALTER TABLE public.product_template
  ADD CONSTRAINT product_template_image_attachment_id_fkey FOREIGN KEY (image_attachment_id)
      REFERENCES public.ir_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL;

ALTER TABLE public.product_template
  ADD CONSTRAINT product_template_image_medium_attachment_id_fkey FOREIGN KEY (image_medium_attachment_id)
      REFERENCES public.ir_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL;

ALTER TABLE public.product_template
  ADD CONSTRAINT product_template_image_small_attachment_id_fkey FOREIGN KEY (image_small_attachment_id)
      REFERENCES public.ir_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE SET NULL;

TRUNCATE public.auditlog_http_request,public.auditlog_http_session,public.auditlog_log,public.auditlog_log_line;
