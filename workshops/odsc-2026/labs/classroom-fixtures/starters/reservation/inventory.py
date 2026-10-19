class Inventory:
 def __init__(self, stock): self.stock=stock; self.requests={}
 def reserve(self, request_id, lines):
  if request_id in self.requests: return True
  for sku,n in lines:
   if self.stock.get(sku,0)<n: return False
   self.stock[sku]-=n
  self.requests[request_id]=dict(lines)
  return True
 def cancel(self, request_id):
  if request_id not in self.requests: return False
  for sku,n in self.requests[request_id].items(): self.stock[sku]+=n
  return True
 def snapshot(self): return self.stock
