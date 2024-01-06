from marshmallow import Schema, fields, validates, ValidationError

class ShapeSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    width = fields.Float(required=False)
    height = fields.Float(required=False)

class SourceSchema(Schema):
    shape = fields.Nested(ShapeSchema, required=True)
    event_element_count = fields.Integer(required=True)

class TargetSchema(Schema):
    shape = fields.Nested(ShapeSchema, required=True)

class ObstacleSchema(Schema):
    id = fields.Integer(required=True)
    shape = fields.Nested(ShapeSchema, required=True)

class RunScenarioInputSchema(Schema):
    model_name = fields.String(required=True)
    source = fields.Nested(SourceSchema, required=True)
    target = fields.Nested(TargetSchema, required=True)
    obstacles = fields.List(fields.Nested(ObstacleSchema), required=False)
    
    @validates('model_name')
    def validate_model_name(self, value):
        valid_model_names = ['osm', 'sfm', 'gnm']
        if value not in valid_model_names:
            raise ValidationError(f"Invalid model_name. Choose from: {', '.join(valid_model_names)}")
