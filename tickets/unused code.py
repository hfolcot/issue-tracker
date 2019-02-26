
		new_update, created = Update.objects.get_or_create(
			content_type=feature.get_content_type,
			object_id=feature.id,
			timestamp=datetime.datetime.now()
			)