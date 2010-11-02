//Set tab to intially be selected when page loads:
//[which tab (1=first tab), ID of tab content to display]:
var initialtab=[1, "sc1"]
 
////////Stop editting////////////////
 
function cascadedstyle(el, cssproperty, csspropertyNS){
if (el.currentStyle)
return el.currentStyle[cssproperty]
else if (window.getComputedStyle){
var elstyle=window.getComputedStyle(el, "")
return elstyle.getPropertyValue(csspropertyNS)
}
}
 
var previoustab=""
 
function expandcontent(cid, aobject){
if (document.getElementById){
highlighttab(aobject)
detectSourceindex(aobject)
if (previoustab!="")
document.getElementById(previoustab).style.display="none"
document.getElementById(cid).style.display="block"
previoustab=cid
if (aobject.blur)
aobject.blur()
return false
}
else
return true
}
 
function highlighttab(aobject){
if (typeof tabobjlinks=="undefined")
collecttablinks()
for (i=0; i<tabobjlinks.length; i++)
tabobjlinks[i].style.backgroundColor=initTabcolor
var themecolor=aobject.getAttribute("theme")? aobject.getAttribute("theme") : initTabpostcolor
aobject.style.backgroundColor=document.getElementById("tabcontentcontainer").style.backgroundColor=themecolor
}
 
function collecttablinks(){
var tabobj=document.getElementById("tablist")
tabobjlinks=tabobj.getElementsByTagName("A")
}
 
function detectSourceindex(aobject){
for (i=0; i<tabobjlinks.length; i++){
if (aobject==tabobjlinks[i]){
tabsourceindex=i //source index of tab bar relative to other tabs
break
}
}
}
 
function do_onload(){
var cookiename=(typeof persisttype!="undefined" && persisttype=="sitewide")? "tabcontent" : window.location.pathname
var cookiecheck=window.get_cookie && get_cookie(cookiename).indexOf("|")!=-1
collecttablinks()
initTabcolor=cascadedstyle(tabobjlinks[1], "backgroundColor", "background-color")
initTabpostcolor=cascadedstyle(tabobjlinks[0], "backgroundColor", "background-color")
if (typeof enablepersistence!="undefined" && enablepersistence && cookiecheck){
var cookieparse=get_cookie(cookiename).split("|")
var whichtab=cookieparse[0]
var tabcontentid=cookieparse[1]
expandcontent(tabcontentid, tabobjlinks[whichtab])
}
else
expandcontent(initialtab[1], tabobjlinks[initialtab[0]-1])
}
 
if (window.addEventListener)
window.addEventListener("load", do_onload, false)
else if (window.attachEvent)
window.attachEvent("onload", do_onload)
else if (document.getElementById)
window.onload=do_onload

