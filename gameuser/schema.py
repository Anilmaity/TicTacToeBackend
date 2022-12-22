import datetime
import math

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
import graphql_jwt
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

from TicTacToeBackend import settings

from .models import Game, Gameuser




class GameuserType(DjangoObjectType):
    class Meta:
        model = Gameuser


class GameType(DjangoObjectType):
    class Meta:
        model = Game


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()



class Query(UserQuery, MeQuery, graphene.ObjectType):
    GetGameUser = graphene.List(GameuserType)
    GameDetail = graphene.List(GameuserType)
    Games = graphene.List(GameType)

    GetGameUserbyId = graphene.Field(GameuserType, id=graphene.Int())
    GetGameUserbyusername = graphene.Field(GameuserType, username=graphene.String())

    GetGamebyId = graphene.Field(GameType, id=graphene.Int())


    def resolve_GetGameUser(self, info, **kwargs):
        return Gameuser.objects.all()


    def resolve_GetGameUserbyId(self, info,id, **kwargs):
        return Gameuser.objects.get(id=id)

    def resolve_GetGameUserbyusername(self, info,username, **kwargs):
        return Gameuser.objects.get(username=username)

    def resolve_GameDetail(self, info, **kwargs):
        return Gameuser.objects.all()

    def resolve_Games(self, info, **kwargs):
        return Game.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(GameuserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()


    def mutate(self, info, username, password, email):
        if (User.objects.filter(username=username).exists()):
            user = User.objects.get(username=username)

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

        GU = Gameuser(username=username, password=password, email=email)
        GU.save()

        return CreateUser(user=GU)



class CreateGame(graphene.Mutation):
    game = graphene.Field(GameType)
    message = graphene.String()

    class Arguments:
        email = graphene.String()
        player1_id = graphene.Int()\

    def mutate(self, info, email, player1_id):
        P1 = Gameuser.objects.get(id=player1_id)
        P2 = Gameuser.objects.get(email=email)

        G = Game.objects.filter(player1_id=P1.id, player2_id=P2.id ,game_over=False)

        if (len(G) > 0):
            return CreateGame(message="Game already exists")
        else:
            game = Game(
                name=P1.username + " vs " + P2.username,
                player1_id=player1_id,
                player2_id=P2.id,
                game_state=str(P1.username)+ " turn",
                game_over=False,
                player1_side="X",
                player2_side="O",
                started_by=player1_id,
                gameid=str(player1_id) + str(P2.id),

            )

            game.save()
            P1.Games.add(game)
            P2.Games.add(game)
            P1.save()
            P2.save()


            return CreateGame(game=game,message="Game created")

class UpdateGame(graphene.Mutation):
    game = graphene.Field(GameType)
    message = graphene.String()

    class Arguments:
        gameid = graphene.Int()
        position = graphene.Int()
        player = graphene.Int()

    def mutate(self, info, gameid, position,player):
        game = Game.objects.get(id=gameid)

        P = Gameuser.objects.get(id=player)
        if P.id == game.player1_id:
            side = game.player1_side
            N_P = Gameuser.objects.get(id=game.player2_id)
        else:
            side = game.player2_side
            N_P = Gameuser.objects.get(id=game.player1_id)

        ttt = game.tictactoe
        if(ttt[position] == "-"):
            ttt = ttt[:position] + side + ttt[position + 1:]
            game.tictactoe = ttt
            game.current_player = N_P.id
            game.game_state = str(N_P.username) + " turn"
            game.save()
            return UpdateGame(game=game,message="Move made")


        else:
            message = "Position already taken"
            return UpdateGame(game=game,message=message)

    # def checkwinconditions(self,ttt):
    #





class Mutation(AuthMutation, graphene.ObjectType):
    create_game = CreateGame.Field()
    update_game = UpdateGame.Field()
    delete_game = mutations.ObtainJSONWebToken.Field()

    CreateUser = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
