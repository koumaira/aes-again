/* AES Again – File tab surgical patch (no style changes). */
(function(){
  function need(url){
    return new Promise(function(res,rej){
      var s=document.createElement('script');
      s.src=url; s.onload=res; s.onerror=function(){rej(new Error('Failed to load '+url))};
      document.head.appendChild(s);
    });
  }
  function $(sel){ return document.querySelector(sel); }
  function byText(txt){
    txt = (txt||'').trim().toLowerCase();
    var els = Array.from(document.querySelectorAll('button,[role="tab"],a,.tab'));
    return els.find(function(el){ return (el.textContent||'').trim().toLowerCase()===txt; });
  }
  function ensurePaneFile(){
    var pane = document.getElementById('pane-file');
    if(pane) return pane;
    var textPane = document.getElementById('pane-text') || byText('text')?.closest('[id]') || document.body;
    pane = document.createElement('div');
    pane.id = 'pane-file';
    pane.style.display = 'none';
    pane.innerHTML = '<div style="display:flex;flex-direction:column;gap:10px"><input id="file-input" type="file" multiple><div id="file-list" style="opacity:.75;font-size:12px"></div><div><button id="zip-btn">Download ZIP</button></div></div>';
    textPane.parentNode.insertBefore(pane, textPane.nextSibling);
    return pane;
  }
  function u8ToWA(u8){ var w=[],i; for(i=0;i<u8.length;i++) w[i>>>2] |= u8[i] << (24-(i%4)*8); return CryptoJS.lib.WordArray.create(w,u8.length); }
  function waToU8(wa){ var w=wa.words,b=wa.sigBytes,u8=new Uint8Array(b); for(var i=0;i<b;i++) u8[i]=(w[i>>>2]>>>(24-(i%4)*8))&255; return u8; }
  function hexToWA(h){ return CryptoJS.enc.Hex.parse((h||'').replace(/\s+/g,'')); }
  function modeObj(name){
    switch((name||'').toLowerCase()){
      case 'cbc': return CryptoJS.mode.CBC;
      case 'ecb': return CryptoJS.mode.ECB;
      case 'cfb': return CryptoJS.mode.CFB;
      case 'ofb': return CryptoJS.mode.OFB;
      case 'ctr': return CryptoJS.mode.CTR;
      default: return CryptoJS.mode.CBC;
    }
  }
  function padZeroCount(u8){
    var block=16, rem=u8.length%block, pad=(rem===0)?0:(block-rem);
    var out=new Uint8Array(u8.length+pad+1); out.set(u8,0); out[out.length-1]=pad; return out;
  }
  function unpadZeroCount(u8){
    if(!u8.length) return u8; var c=u8[u8.length-1]; if(c>16) return u8; return u8.slice(0, Math.max(0,u8.length-1-c));
  }
  function encryptOrDecrypt_bytes(bytes, cfg){
    var key = hexToWA(cfg.keyHex);
    var c = { mode: modeObj(cfg.mode), padding: CryptoJS.pad.NoPadding };
    if(cfg.mode!=='ecb'){
      if((cfg.mode||'').toLowerCase()==='ctr') c.counter = hexToWA(cfg.ctrHex);
      else c.iv = hexToWA(cfg.ivHex);
    }
    var input = bytes;
    if((cfg.op||'enc').toLowerCase()==='enc' && (cfg.mode||'cbc').toLowerCase()!=='ctr') input = padZeroCount(bytes);
    var waIn = u8ToWA(input);
    var waOut;
    if((cfg.op||'enc').toLowerCase()==='enc'){
      waOut = CryptoJS.AES.encrypt(waIn, key, c).ciphertext;
    }else{
      var params = CryptoJS.lib.CipherParams.create({ciphertext: waIn});
      waOut = CryptoJS.AES.decrypt(params, key, c);
    }
    var out = waToU8(waOut);
    if((cfg.op||'enc').toLowerCase()==='dec' && (cfg.mode||'cbc').toLowerCase()!=='ctr') out = unpadZeroCount(out);
    return out;
  }
  function getVal(id, fallback){
    var el = document.getElementById(id);
    if(el && 'value' in el) return el.value;
    return fallback;
  }
  function currentCfg(){
    return {
      mode: getVal('mode','cbc'),
      op:   getVal('op','enc'),
      keyHex: getVal('key','2b7e151628aed2a6abf7158809cf4f3c'),
      ivHex:  getVal('iv','00000000000000000000000000000000'),
      ctrHex: getVal('ctr','f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff')
    };
  }
  function wireTabs(){
    var textTab = document.getElementById('tab-text') || byText('text');
    var fileTab = document.getElementById('tab-file') || byText('file');
    var textPane = document.getElementById('pane-text') || (textTab ? textTab.closest('[id]') : null);
    var filePane = ensurePaneFile();
    function show(which){
      if(textTab) textTab.classList.toggle('active', which==='text');
      if(fileTab) fileTab.classList.toggle('active', which==='file');
      if(textPane) textPane.style.display = (which==='text'?'block':'none');
      if(filePane) filePane.style.display = (which==='file'?'block':'none');
    }
    if(textTab) textTab.addEventListener('click', function(e){ e.preventDefault(); show('text'); });
    if(fileTab) fileTab.addEventListener('click', function(e){ e.preventDefault(); show('file'); });
    show('text');
  }
  function wireFiles(){
    var input = document.getElementById('file-input');
    var list = document.getElementById('file-list');
    var zipBtn = document.getElementById('zip-btn');
    if(!input || !zipBtn || !list) return;
    input.addEventListener('change', function(){
      if(!input.files || !input.files.length){ list.textContent=''; return; }
      list.textContent = 'Selected: ' + Array.from(input.files).map(function(f){return f.name+' ('+f.size+' B)'}).join(', ');
    });
    zipBtn.addEventListener('click', async function(){
      if(!input.files || !input.files.length){ list.textContent='No files selected.'; return; }
      if(typeof JSZip==='undefined'){ list.textContent='JSZip not loaded'; return; }
      var cfg = currentCfg();
      var zip = new JSZip();
      var processed = 0;
      for (const f of input.files){
        var buf = await f.arrayBuffer();
        var out = encryptOrDecrypt_bytes(new Uint8Array(buf), cfg);
        var ext = ((cfg.op||'enc').toLowerCase()==='enc')?'.enc':'.dec';
        zip.file(f.name+ext, out);
        processed++;
      }
      var blob = await zip.generateAsync({type:'blob'});
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'aes-again-output.zip';
      a.click();
      URL.revokeObjectURL(a.href);
      list.textContent = 'Processed ' + processed + ' files → downloaded ZIP.';
    });
  }
  var wants = [];
  if(!window.CryptoJS) wants.push('https://cdn.jsdelivr.net/npm/crypto-js@4.2.0/crypto-js.min.js');
  if(!window.JSZip)    wants.push('https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js');
  (wants.length?Promise.all(wants.map(need)):Promise.resolve()).then(function(){
    wireTabs();
    wireFiles();
  }).catch(function(err){ console.error('Patch init failed:', err); });
})();