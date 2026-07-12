const i=t=>{if(!t.startsWith("/")||t.startsWith("//")||t.startsWith("/\\"))return!1;try{return new URL(t,window.location.origin).origin===window.location.origin}catch{return!1}};export{i};
