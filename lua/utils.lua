local _m = {}

local Set = function(list)
  local set = {}
  for _, l in ipairs(list) do set[l] = true end
  return set
end

local WHITE_DOMAIN = Set({'.*?baidu\\.com$'})
local DEMO_URL_PATTERN = '.*demo\\..+'

local is_match_white_domain = function(domain)
  for k, v in pairs(WHITE_DOMAIN) do
    local m, err = ngx.re.match(domain, '.*baidu.com')
    if m and m[0] == domain then
      return true
    end
  end
  return false
end

_m.is_white = function(domain)
  if WHITE_DOMAIN[domain] then
    return true
  elseif is_match_white_domain(domain) then
    return true
  else
    return false
  end
end

_m.is_local_host = function(referer_domian, domain)
  if referer_domian == domain then
    return true
  else
    return false
  end
end

_m.is_demo_url = function(domain)
  local m, err = ngx.re.match(domain, DEMO_URL_PATTERN)
  if m and m[0] == domain then
    return true
  else
    if err then
      ngx.log(ngx.ERR, 'error: ', err)
    end
    return false
  end
end

return _m
