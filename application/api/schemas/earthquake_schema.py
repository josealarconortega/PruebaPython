from application.api.database import ma


class earthquakeSchema(ma.ModelSchema):
    class Meta:
        fields = ("create_at", "fecha_inicio", "fecha_fin", "magnitud_min", "magnitud_max", "salida")

earthquake_schema = earthquakeSchema()
earthquakes_schema = earthquakeSchema(many=True)