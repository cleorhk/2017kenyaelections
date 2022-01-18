from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class President(Resource):
    def get(self):
        data = pd.read_csv('presda1-converted.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('County_code', required=True)  # add args
        parser.add_argument('County', required=True)
        parser.add_argument('Voting Block', required=True)
        parser.add_argument('Block_code', required=True)
        parser.add_argument('Registered Voters', required=True)
        parser.add_argument('Valid votes', required=True)
        parser.add_argument('Kenyatta', required=True)
        parser.add_argument('Raila', required=True)
        parser.add_argument('Spoilt votes', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('presda1-converted.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'County_code': [args['userId']],
                'County': [args['County']],
                'Voting Block': [args['Voting Block']],
                'Block_code ': [args['Block_code']],
                'Registered Voters': [args['Registered Voters']],
                'Valid Votes': [args['Valid Votes']],
                'Kenyatta': [args['Kenyatta']],
                'Raila': [args['Raila']],
                'Spoilt Votes': [args['Spoilt Votes']]

            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('County_code', required=True)  # add args
        parser.add_argument('County', required=True)
        parser.add_argument('Voting Block', required=True)
        parser.add_argument('Block_code', required=True)
        parser.add_argument('Registered Voters', required=True)
        parser.add_argument('Valid votes', required=True)
        parser.add_argument('Kenyatta', required=True)
        parser.add_argument('Raila', required=True)
        parser.add_argument('Spoilt votes', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('presda1-converted.csv')

        if args['County_code'] in list(data['County_code']):
            # evaluate strings of lists to lists !!! never put something like this in prod
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )

            # select our county
            county_data = data[data['County_code'] == args['County_code']]

            # update user's locations
            county_data['County'] = county_data['County'].values[0] \
                .append(args['County'])
            # update the voting block
            county_data['Voting Block'] = county_data['Voting Block'].values[0] \
                .append(args['Voting Block'])
            # update the Registered voters
            county_data['Registered voters'] = county_data['Registered voters'].values[0] \
                .append(args['Registered voters'])
            # update valid votes
            county_data['Valid votes'] = county_data['Valid votes'].values[0] \
                .append(args['Valid votes'])
            # update Kenyatta
            county_data['Kenyatta'] = county_data['Kenyatta'].values[0] \
                .append(args['Kenyatta'])
            # update Raila
            county_data['Raila'] = county_data['Raila'].values[0] \
                .append(args['Raila'])
            # update spoilt votes
            county_data['Spoilt votes'] = county_data['Spoilt votes'].values[0] \
                .append(args['Spoilt votes'])

            # save back to CSV
            data.to_csv('presda1-converted.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the county code does not exist
            return {
                       'message': f"'{args['County_code']}' data not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('County_code', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('presda1-converted.csv')

        if args['County_code'] in list(data['County_code']):
            # remove data entry matching given userId
            data = data[data['County_code'] != args['County_code']]

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                       'message': f"'{args['County_code']}' data not found."
                   }, 404

class VoteReg(Resource):
    def get(self):
        data = pd.read_csv('iebc.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('iebc.csv')

        if args['userId'] in list(data['userId']):
            return {
                       'message': f"'{args['userId']}' already exists."
                   }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': [args['userId']],
                'name': [args['name']],
                'city': [args['city']],
                'locations': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('iebc.csv')

        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists !!! never put something like this in prod
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])

            # save back to CSV
            data.to_csv('iebc.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


api.add_resource(President, '/elec')  # add endpoints
api.add_resource(VoteReg, '/reg')

if __name__ == '__main__':
    app.run()  # run our Flask app