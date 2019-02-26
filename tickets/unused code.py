
		new_update, created = Update.objects.get_or_create(
			content_type=feature.get_content_type,
			object_id=feature.id,
			timestamp=datetime.datetime.now()
			)

		def voting_view(request, object_id, vote_type, content_type):
	"""
	Rate the current ticket
	"""
	if vote_type == 1:
		vote_boolean = True
	else:
		vote_boolean = False
	c_type = ContentType.objects.get(model=content_type)
	print(c_type)
	if c_type == 'bugticket':
		bug = get_object_or_404(BugTicket, id=object_id)
		if vote_boolean == True:
			
	new_vote, created = Vote.objects.get_or_create(
							positive_vote=vote_boolean,
							user=request.user,
							object_id=object_id,
							content_type=c_type
							)
	messages.success(request, f"Thank you for voting")
	return redirect(bug_ticket_view, object_id)