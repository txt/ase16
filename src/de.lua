_tostring = tostring

function tostring(x,seen)
  local out  = {}
  seen = seen or {}
  local function go(y)
    if type(y)=="table" then
      if   seen[y]
      then out[#out+1] = "..."
      else seen[y] = y
           out[#out+1] = "{"
           local sep=""
           for z,v in pairs(y) do
             out[#out+1] =  sep .. _tostring(z) .. "=" .. tostring(v,seen)
             sep =", "
           end 
           out[#out+1] = "}" end
    else
      out[#out+1] = _tostring(y)
  end end 
  go(x)
  return table.concat(out)
end

r = math.random

function any(t) return t[ r(#t) ] end

local function has(t, x)
  for _,y in pairs(t) do
    if y == x then 
      return true
  end end
  return false
end

--------------------------------------
local de={}

function de.less(x,y) return x < y end
function de.more(x,y) return x > y end

function de.num(t) 
  t.lo = t.lo or 0
  t.hi = t.hi or 1
  return t
end

function de.sym(t)
  t.all = t.all or {}
end

function de.obj(t)  
  de.num(t)
  t.better = t.better or less
  t.get    = t.get or de.numAny
  return t
end

function de.xy(t)
  t   = t or {}
  t.x = t.x or {}
  t.y = t.y or {}
  return t
end
-------------------------------
function de.model(t)
  de.xy(t)
  t.ok = t.ok   or (function (_) return True end)
end

function de.ok(i, t, wants)
  local function num()
    assert t[i] >= wants[i].lo and t[i] <= wants[j].hi end
  local function sym()
    assert has(wants[i].all, t[i]) end
   if t[i] ~= nil then
     f = (t.all and num or sym)()
end end 

function de.oks(wants,t)
  for i = 1,#wants.x do de.ok(i, t.x, wants.x) end 
  for i = 1,#wants.y do de.ok(i, t.y, wants.y) end
end

function de.any(want)
  local function num() return want.lo + r()*(want.hi - want.lo) end
  local function sym() return any(want.all) end
  return (want.all and sym or num)()
end

function de.model2decs(wants)
  local got = de.xy()
  for k,want in pairs(wants.x) do
    got.x[k] = de.any(want)
  end
  return got
end

function de.decs2objs(wamt,t)
  if t.objs then return t end
  for y,v in pairs(want.y) do got.x[y] = de.numAny(v) end
  return t
end

function de.evolve(m)
  local fronter={}
  for i=1,#m.decs*10 do
    frontier[i] = de.model2decs(m)
  end
    
end

function de.bdom(objs,y1s,y2s)
  local betters=0
  for i=1,#objs do
    local better = objs[i].want
    local y1, y2 = y1s[i], y2s[i]
    if    better( y1s[i], y2s[i])
    then  betters = betters + 1
    elseif y1 ~= y2 then return False end
  end
  return betters > 0
end

function m1()
  function get1(xy)
    return (xy[1] + xy[2])^2
  end
  local s,n,o = de.sym, de.num,de.obj
  return de.model{
    decs={
      s{name="day", all={"mon","tue","wed","thr","fri","sat","sun"}}
      d{name="d1", lo=10, hi=40},
      d{name="d2", lo=30, hi=50}
    } ,
    objs={
      o{name="o1",get = get1},
      o{name="o2",want = more}
  }}

  -- want got, seen
