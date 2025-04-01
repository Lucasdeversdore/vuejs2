<template>
  <div>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <div class="card bg-light mb-3">
      <h1>Les Questionnaires</h1>
      <div class="card" v-for="questionnaire in questionnaires.questionnaires" :key="questionnaire.id">
        <QuestionnaireItem :questionnaire="questionnaire" @remove="removeQuestionnaire" @modify="editQuestionnaire"
          @consult="consultQuestions" @removeQ="removeQuestion" @afficheForm="afficheForm" @addQ="addQuestion"
          @modifyQ="editQuestion" />
      </div>
      <input type="button" value="Ajouter un Questionnaire" @click="addQuestionnaire">
    </div>
  </div>
</template>

<script>
import QuestionnaireItem from './components/QuestionnaireItem.vue';

export default {
  components: {
    QuestionnaireItem
  },
  data() {
    return {
      questionnaires: []
    };
  },
  mounted() {
    this.fetchQuestionnaire();
  },
  methods: {
    fetchQuestionnaire() {
      fetch("http://127.0.0.1:5000/quiz/api/v1.0/questionnaires")
        .then(response => response.json())
        .then(data => {
          this.questionnaires = data;
        })
        .catch(error => {
          console.error('There was an error!', error);
        });
    },
    removeQuestionnaire(payload) {
      const index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
      if (index !== -1) {
        this.questionnaires.questionnaires.splice(index, 1);
        fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${payload.id}`, {
          method: 'DELETE'
        }).then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    },
    editQuestionnaire(payload) {
      let newName = prompt("Entrez le nouveau nom du questionnaire");
      let index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
      if (index !== -1 && newName !== null && newName !== "" && newName.trim() !== "") {
        this.questionnaires.questionnaires[index].name = newName;
        fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${payload.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newName
          })
        }).then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    },
    consultQuestions(payload) {
      let index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
      let name = this.questionnaires.questionnaires[index].name;
      let div = document.getElementsByClassName(name)[0];
      let bouton = document.getElementById("consult-" + payload.id);
      if (div.style.display === "none") {
        div.style.display = "block";
        bouton.value = "Fermer";
      } else {
        div.style.display = "none";
        bouton.value = "Consulter";
      }
    },
    removeQuestion(payload) {
      let index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
      let questionIndex = this.questionnaires.questionnaires[index].questions.findIndex(question => question.id === payload.questionId);
      if (questionIndex !== -1) {
        this.questionnaires.questionnaires[index].questions.splice(questionIndex, 1);
        fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questions/${payload.questionId}`, {
          method: 'DELETE'
        }).then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    },
    afficheForm(payload) {
      let button = document.getElementById("button-addQ-" + payload.id);
      let div = document.getElementById("divForm-" + payload.id);
      if (div.style.display === "none") {
        div.style.display = "block";
        button.value = "Annuler";
      } else {
        div.style.display = "none";
        button.value = "Ajouter une question";
      }
      let radioSimple = document.getElementById("simple-" + payload.id);
      let radioMultiple = document.getElementById("multiple-" + payload.id);

      radioSimple.addEventListener("click", function () {
        let choix3 = document.getElementById("choix3-" + payload.id);
        let choix4 = document.getElementById("choix4-" + payload.id);
        choix3.style.display = "none";
        choix4.style.display = "none";
      });

      radioMultiple.addEventListener("click", function () {
        let choix3 = document.getElementById("choix3-" + payload.id);
        let choix4 = document.getElementById("choix4-" + payload.id);
        choix3.style.display = "block";
        choix4.style.display = "block";
      });
    },
    getMaxIdQuestion() {
      let maxId = 0;
      this.questionnaires.questionnaires.forEach(questionnaire => {
        questionnaire.questions.forEach(question => {
          if (question.id > maxId) {
            maxId = question.id;
          }
        });
      });
      return maxId;
    },
    sendFetchRequest(payload) {
      let question = {};
      if (payload.type === "simple") {
        question = {
          "choix1": payload.choices[0],
          "choix2": payload.choices[1]
        };
      } else {
        question = {
          "choix1": payload.choices[0],
          "choix2": payload.choices[1],
          "choix3": payload.choices[2],
          "choix4": payload.choices[3]
        };
      }
      fetch(`http://127.0.0.1:5000/quiz/api/v1.0/${payload.id}/questions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: question,
          question_type: payload.type,
          questionnaire_id: payload.id,
          title: payload.title
        })
      }).then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    },
    addQuestion(payload) {
      let button = document.getElementById("button-addQ-" + payload.id);
      let div = document.getElementById("divForm-" + payload.id);
      if (div.style.display === "none") {
        div.style.display = "block";
        button.value = "Annuler";
      } else {
        div.style.display = "none";
        button.value = "Ajouter une question";
      }
      let question = {};
      if (payload.type === "simple") {
        payload.choices[2] = "simple";
        payload.choices[3] = "simple";
      }
      if (payload.title !== "" && payload.title.trim() !== "" && payload.choices[0] !== "" && payload.choices[0].trim() !== "" && payload.choices[1] !== "" && payload.choices[1].trim() !== "" && payload.choices[2] !== "" && payload.choices[2].trim() !== "" && payload.choices[3] !== "" && payload.choices[3].trim() !== "") {
        let index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
        if (payload.type === "simple") {
          question = { "choix1": payload.choices[0], "choix2": payload.choices[1] }
          this.questionnaires.questionnaires[index].questions.push({
            id: this.getMaxIdQuestion() + 1,
            question: question,
            question_type: payload.type,
            questionnaire_id: payload.id,
            title: payload.title
          });
          this.sendFetchRequest(payload);
        } else {
          question = { "choix1": payload.choices[0], "choix2": payload.choices[1], "choix3": payload.choices[2], "choix4": payload.choices[3] }
          this.questionnaires.questionnaires[index].questions.push({
            id: this.getMaxIdQuestion() + 1,
            question: question,
            question_type: payload.type,
            questionnaire_id: payload.id,
            title: payload.title
          });
          this.sendFetchRequest(payload);
        }
      }
    },
    editQuestion(payload) {
      let newName = prompt("Entrez le nouveau titre de la question");
      let index = this.questionnaires.questionnaires.findIndex(questionnaire => questionnaire.id === payload.id);
      let questionIndex = this.questionnaires.questionnaires[index].questions.findIndex(question => question.id === payload.questionId);
      if (index !== -1 && questionIndex !== -1 && newName !== null && newName !== "" && newName.trim() !== "") {
        this.questionnaires.questionnaires[index].questions[questionIndex].title = newName;
        fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questions/${payload.questionId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: newName
          })
        }).then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    },
    addQuestionnaire() {
      let name = prompt("Entrez le nom du questionnaire");
      if (name !== null && name !== "" && name.trim() !== "") {
        fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: name
          })
        }).then(response => response.json())
          .then(data => {
            this.questionnaires.questionnaires.push(data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    }
  }
}
</script>