import pytest


class TestRootEndpoint:
    """Testes para o endpoint raiz"""
    
    def test_root_redirect(self, client):
        """Testa se o endpoint / redireciona para /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Testes para GET /activities"""
    
    def test_get_all_activities(self, client):
        """Testa se retorna todas as atividades"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Verificar estrutura de uma atividade
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
    
    def test_activities_contain_expected_data(self, client):
        """Testa se as atividades contêm os dados esperados"""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Testes para POST /activities/{activity_name}/signup"""
    
    def test_signup_success(self, client):
        """Testa inscrição bem-sucedida"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Signed up newstudent@mergington.edu for Chess Club" == data["message"]
    
    def test_signup_duplicate_email(self, client):
        """Testa erro ao tentar inscrever email já cadastrado"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "Student already signed up for this activity" == data["detail"]
    
    def test_signup_activity_not_found(self, client):
        """Testa erro ao tentar inscrever em atividade inexistente"""
        response = client.post(
            "/activities/NonExistent/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "Activity not found" == data["detail"]
    
    def test_signup_activity_full(self, client):
        """Testa erro ao tentar inscrever em atividade cheia"""
        # Primeiro, preencher uma atividade pequena
        small_activity = "Robotics Club"  # max 18, já tem 1
        
        # Adicionar participantes até encher
        for i in range(17):  # 1 já existe, adicionar 17 para chegar a 18
            email = f"student{i}@mergington.edu"
            response = client.post(
                f"/activities/Robotics%20Club/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Agora tentar adicionar mais um deve falhar
        response = client.post(
            "/activities/Robotics%20Club/signup?email=overflow@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "Activity is full" == data["detail"]


class TestUnregisterEndpoint:
    """Testes para DELETE /activities/{activity_name}/signup"""
    
    def test_unregister_success(self, client):
        """Testa desinscrição bem-sucedida"""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Unregistered michael@mergington.edu from Chess Club" == data["message"]
    
    def test_unregister_not_signed_up(self, client):
        """Testa erro ao tentar desinscrever email não cadastrado"""
        response = client.delete(
            "/activities/Chess%20Club/signup?email=notsigned@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        assert "Student not signed up for this activity" == data["detail"]
    
    def test_unregister_activity_not_found(self, client):
        """Testa erro ao tentar desinscrever de atividade inexistente"""
        response = client.delete(
            "/activities/NonExistent/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "Activity not found" == data["detail"]


class TestIntegration:
    """Testes de integração para verificar estado consistente"""
    
    def test_signup_then_unregister(self, client):
        """Testa inscrição seguida de desinscrição"""
        email = "integration@test.edu"
        activity = "Programming Class"
        
        # Inscrever
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verificar se foi adicionado
        response = client.get("/activities")
        data = response.json()
        assert email in data[activity]["participants"]
        
        # Desinscrever
        response = client.delete(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verificar se foi removido
        response = client.get("/activities")
        data = response.json()
        assert email not in data[activity]["participants"]