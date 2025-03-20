struct Node* mergeAndSort(struct Node* head1, struct Node* head2) {
    struct Node* merged = NULL;
    struct Node* tempMerged = NULL;

    
    while (head1 != NULL && head2 != NULL) {
        struct Node* newNode = NULL;
        
        if (head1->data < head2->data) {
            newNode = head1;
            head1 = head1->next;
        } else {
            newNode = head2;
            head2 = head2->next;
        }

        if (merged == NULL) {
            merged = newNode;
            tempMerged = merged;
        } else {
            tempMerged->next = newNode;
            tempMerged = tempMerged->next;
        }
    }


    if (head1 != NULL) {
        tempMerged->next = head1;
    } else if (head2 != NULL) {
        tempMerged->next = head2;
    }

    return merged;
}