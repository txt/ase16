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

function less(x,y) return x < y end
function more(x,y) return x > y end
function yes(...) return True end

--------------------------------------
local want={}

function ako(t,o)
  t = t or {}
  t.__ako == o
  o(t)
  return t
end

function xy0(t)
  t.x = t.x or {}
  t.y = t.y or {}
end

function want.num0(t)
  t.lo = t.lo or 0
  t.hi = t.hi or 1
end

function want.sym0(t)
  t.all = t.all or {}
end

function want.obj0(t)  
  t        = ako(t, want.num0)
  t.better = t.better or less
  t.get    = t.get or de.numAny
end

function want.model0(t)
  t = ako(t, xy0)
  t.ok = t.ok or yes
end

function want.any(t)
  local function num() return t.lo + r()*(t.hi - t.lo) end
  local function sym() return any(t.all) end
  if t.__get then
    return t.__get(t)
  else
    return (t.all and sym or num)()
end end

-------------------------------
got={}

function got.ok(i, t, wants)
  local function num()
    assert (t[i] >= wants[i].lo and t[i] <= wants[j].hi ) end
  local function sym()
    assert (has(wants[i].all, t[i])) end
   if t[i] ~= nil then
     f = (t.all and num or sym)()
end end 

function got.oks(wants,t)
  for i = 1,#wants.x do got.ok(i, t.x, wants.x) end 
  for i = 1,#wants.y do got.ok(i, t.y, wants.y) end
end



function de.model2decs(wants)
  local got = de.xy0()
  for k,want1 in pairs(wants.x) do
    got.x[k] = want.any(want1)
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
  local s,n,o = want.sym0, want.num0,want.obj0
  return de.model{
    decs={
      s{name="day", all={"mon","tue","wed","thr","fri","sat","sun"}},
      d{name="d1", lo=10, hi=40},
      d{name="d2", lo=30, hi=50}
    } ,
    objs={
      o{name="o1",get = get1},
      o{name="o2",want = more}
  }}
end
