import{fn as i,fo as l}from"./index-S79wb68G.js";const s=" ",a=`

`,p=/^\*\*(?=\S)([^\n]*?\S)\*\*/;class k extends l{emStrong(n,t,c){const o=super.emStrong(n,t,c);if(o)return o;const r=p.exec(n);if(r?.[1])return{type:"strong",raw:r[0],text:r[1],tokens:this.lexer.inlineTokens(r[1])}}}const u=()=>new k,x=u();function f(e){return e.replace(/^&nbsp;$/gm,s).replace(/\n{3,}/g,n=>{const t=Math.floor((n.length-2)/2);return a+`${s}${a}`.repeat(t)})}const g=e=>i.lex(f(e),{tokenizer:x});export{s as B,u as c,g as p};
