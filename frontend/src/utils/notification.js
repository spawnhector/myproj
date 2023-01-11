
export function openNotification(root,position = null, border, data,progress = null,onDestroy= null,duration = 'none') {
    const noti = root.$vs.notification({
        progress: 0,
        duration,
        border,
        position,
        title: data.title,
        text: data.text,
        onDestroy: onDestroy
    })
    root.$watch('progress',(newprog)=>{
        if(newprog == 100) noti.close();
        noti.changeProgress(newprog)
    })
}