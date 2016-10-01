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

--------------------------------------
local de={}

function de.less(x,y) return x < y end
function de.more(x,y) return x > y end

function de.num(t) 
  t.lo = t.lo or 0
  t.hi = t.hi or 1
  return t
end

function de.dec(t) 
  de.num(t)
  return t
end

function de.obj(t)  
  de.num(t)
  t.better = t.better or less
  t.get  = t.get or de.numAny
  return t
end

function de.xy(t)
  t= t or {}
  t.x = t.x or {}
  t.y = t.y or {}
  return t
end
-------------------------------
function de.model(t)
  de.xy(t)
  t.ok   = t.ok   or (function (_) return True)
end

function de.numAny(n)
  return n.lo + r()*(n.hi - n.lo)
end

function de.model2decs(want)
  local got = de.xy()
  for x,v in pairs(want.x) do
    got.x[k] = de.numAny(v)
  end
  return got
end

function de.decs2objs(t)
  if t.objs then return t end
  

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
  local d,o = de.dec,de.obj
  return de.model{
    decs={
      d{name="d1",lo=10,hi=40},
      d{name="d2",lo=30,hi=50}
    } ,
    objs={
      o{name="o1",get = get1},
      o{name="o2",want = more}
  }}

  -- want got, seen
