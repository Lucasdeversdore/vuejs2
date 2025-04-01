<template>
    <div class="d-flex flex-column">
        <h3>{{ questionnaire.name }}</h3>
        <div :class="questionnaire.name" style="display: none;">
            <div v-for="question in questionnaire.questions" :key="question.id" :id="`${question.id}`">
                <p>{{ question.title }}</p>
                <div v-if="question.question_type === 'simple'" class="d-flex justify-content-around">
                    <label>{{ question.question.choix1 }}</label>
                    <input type="radio" :name="`question-${question.id}`" :value="question.question.choix1">
                    <input type="radio" :name="`question-${question.id}`" :value="question.question.choix2">
                    <label>{{ question.question.choix2 }}</label>
                    <input type="button" class="btn btn-danger" value="Supprimer" @click="supprQ(question.id)">
                    <input type="button" class="btn btn-warning" value="Modifier" @click="modifQ(question.id)">

                </div>
                <div v-else-if="question.question_type === 'multiple'" class="d-flex justify-content-around">
                    <div v-for="(choice, index) in question.question" :key="index">
                        <label>{{ choice }}</label>
                        <input type="checkbox" :name="`question-${question.id}`" :value="choice">
                    </div>
                    <input type="button" class="btn btn-danger" value="Supprimer" @click="supprQ(question.id)">
                    <input type="button" class="btn btn-warning" value="Modifier" @click="modifQ(question.id)">
                </div>
            </div>
            <input type="button" class="btn btn-primary" value="Ajouter une question"
                :id="`button-addQ-${questionnaire.id}`" @click="afficheForm">
            <div style="display: none;" :id="`divForm-${questionnaire.id}`">
                <form action="" :id="`form-${questionnaire.id}`">
                    <input type="radio" name="typeQ" :id="`simple-${questionnaire.id}`" value="simple">
                    <label for="simple">Question simple</label>
                    <input type="radio" name="typeQ" :id="`multiple-${questionnaire.id}`" value="multiple" checked>
                    <label for="multiple">Question à choix multiples</label>
                </form>
                <div :id="`choix-${questionnaire.id}`" class="d-flex flex-wrap justify-content-center"
                    style="width: 10vw; margin-left: auto; margin-right: auto;">
                    <input type="text" placeholder="Titre" :id="`question-${questionnaire.id}`">
                    <input type="text" placeholder="Choix 1" :id="`choix1-${questionnaire.id}`">
                    <input type="text" placeholder="Choix 2" :id="`choix2-${questionnaire.id}`">
                    <input type="text" placeholder="Choix 3" :id="`choix3-${questionnaire.id}`">
                    <input type="text" placeholder="Choix 4" :id="`choix4-${questionnaire.id}`">
                    <input type="button" class="btn btn-primary" value="Ajouter" @click="addQ">
                </div>
            </div>
        </div>
        <div class="d-flex flex-row mt-2 justify-content-around">
            <input type="button" class="btn btn-danger" value="Supprimer" @click="suppr">
            <input type="button" class="btn btn-warning" value="Modifier" @click="modif">
            <input type="button" class="btn btn-primary" value="Consulter" @click="consult"
                :id="`consult-${questionnaire.id}`">
        </div>
    </div>
</template>

<script>
export default {
    props: {
        questionnaire: Object
    },
    data() {
        return {
            selectedChoices: {}
        };
    },
    methods: {
        suppr() {
            this.$emit('remove', { id: this.questionnaire.id });
        },
        modif() {
            this.$emit('modify', { id: this.questionnaire.id });
        },
        consult() {
            this.$emit('consult', { id: this.questionnaire.id });
        },
        supprQ(questionId) {
            this.$emit('removeQ', { id: this.questionnaire.id, questionId: questionId });
        },
        afficheForm() {
            this.$emit('afficheForm', { id: this.questionnaire.id });
        },
        addQ() {
            let form = document.getElementById(`form-${this.questionnaire.id}`);
            let type = form.querySelector('input[type="radio"]:checked').value;
            let title = document.getElementById(`question-${this.questionnaire.id}`).value;
            let choix1 = document.getElementById(`choix1-${this.questionnaire.id}`).value;
            let choix2 = document.getElementById(`choix2-${this.questionnaire.id}`).value;
            let choix3 = document.getElementById(`choix3-${this.questionnaire.id}`).value;
            let choix4 = document.getElementById(`choix4-${this.questionnaire.id}`).value;
            let choices = [choix1, choix2];
            if (type === 'multiple') {
                choices.push(choix3, choix4);
            }
            this.$emit('addQ', { id: this.questionnaire.id, type, title, choices });
        },
        modifQ(questionId) {
            this.$emit('modifyQ', { id: this.questionnaire.id, questionId: questionId });
        }
    },
    emits: ['remove', 'modify', 'consult', 'removeQ', 'afficheForm', 'addQ', 'modifyQ']
}
</script>
