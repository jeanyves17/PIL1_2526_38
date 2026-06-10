const API = {
  base: "",
  token: () => localStorage.getItem("token"),
  setToken: (t) => localStorage.setItem("token", t),
  clear: () => localStorage.removeItem("token"),
  async req(path, opts = {}) {
    const headers = { "Content-Type": "application/json", ...(opts.headers||{}) };
    const t = API.token();
    if (t) headers.Authorization = "Bearer " + t;
    const r = await fetch(API.base + path, { ...opts, headers,
      body: opts.body ? JSON.stringify(opts.body) : undefined });
    const data = await r.json().catch(()=> ({}));
    if (!r.ok) throw new Error(data.error || ("Erreur " + r.status));
    return data;
  },
  get:(p)=>API.req(p),
  post:(p,b)=>API.req(p,{method:"POST",body:b}),
  put:(p,b)=>API.req(p,{method:"PUT",body:b}),
  del:(p)=>API.req(p,{method:"DELETE"}),
};
