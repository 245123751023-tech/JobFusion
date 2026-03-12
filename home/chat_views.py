from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from firebase_admin import db

from .models import NotRequired,Profile

def chat_view(request):
    """Show all users you have chats with"""
    current_user = request.user.username
    chat_ref = db.reference("chats")
    chats = chat_ref.get() or {}
    
    user_chats = set()
    for room_id, messages in chats.items():
        if current_user in room_id:
            parts = room_id.split("_")
            for name in parts:
                if name != current_user:
                    user_chats.add(name)
    
    notreq_obj,k = NotRequired.objects.get_or_create(user=request.user)
    deleted_people = notreq_obj.deleted_chats
    blocked_people = notreq_obj.blocked_chats

    user_chats = {
        chat_person for chat_person in user_chats # here all people,not metter what
        if chat_person not in deleted_people and chat_person not in blocked_people
    }

    final_users = []

    for uname in user_chats:
        try:
            p_obj = Profile.objects.get(user__username=uname)
            final_users.append(p_obj)
        except Profile.DoesNotExist:
            pass

    context = {"final_users": list(final_users),"deleted_users":list(deleted_people),"blocked_users":list(blocked_people)}
    return render(request, "chats.html", context)


def delchat(request,id):
    delper = get_object_or_404(Profile,id=id)
    
    notreq_obj,k = NotRequired.objects.get_or_create(user=request.user)

    current_user = request.user
    current_user_name = current_user.username
    other_user = delper.user.username

    if delper.user.username not in notreq_obj.deleted_chats:
        notreq_obj.deleted_chats.append(delper.user.username)
        notreq_obj.save()  

    room_id = "_".join(sorted([str(current_user_name),str(other_user)]))


    chat_ref = db.reference("chats")
    chats = chat_ref.get() or {}

    if room_id in chats:
        for msg_id,msg in chats[room_id].items():
            if "deletedFor" not in msg:
                msg["deleterFor"] = {
                    current_user_name:False,
                    other_user:False
                }
            
            msg["deletedFor"][current_user_name] = True
            chat_ref.child(room_id).child(msg_id).update({
                "deletedFor":msg["deletedFor"]
            })
    return redirect("chats")

def blockchat(request,id):
    blockper = get_object_or_404(Profile,id=id)

    notreq_obj,k = NotRequired.objects.get_or_create(user=request.user)

    if blockper.user.username not in notreq_obj.blocked_chats:
        notreq_obj.blocked_chats.append(blockper.user.username)
        notreq_obj.save()

    return redirect("chats")
