local net = require 'net.url'
local utils = require 'utils'
local cjson = require 'cjson'

local url_args = ngx.req.get_uri_args()
local redirect_url = url_args['url']
local headers = ngx.req.get_headers()


local get_referer_domain = function(headers)
  local referer = headers['referer']
  local referer_parse_result = net.parse(referer)
  if referer_parse_result then
    local referer_domain = referer_parse_result['host']
    if referer_domain then
      return referer_domain
    end
  end
  return ''
end

if not redirect_url then
  ngx.status = 404
  ngx.say('Not Found')
  ngx.exit(ngx.OK)
end

local result = net.parse(redirect_url)
local domain = result['host']
if not domain then
  ngx.status = 400
  ngx.say('URL param error')
  ngx.exit(ngx.OK)
end

local referer_domain = get_referer_domain(headers)

if utils.is_demo_url(domain) or utils.is_local_host(referer_domain, domain) or utils.is_white(domain) then
  return ngx.redirect(redirect_url)
else
  ngx.status = 404
  ngx.say('Not Found')
  ngx.exit(ngx.OK)
end
