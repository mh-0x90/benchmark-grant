def register_routes(app):
    from . import verify, reports, account, profile, feedback, settings, media, dashboard, account_admin, search

    app.register_blueprint(feedback.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(media.bp)
    app.register_blueprint(account_admin.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(reports.bp)
