package com.apo.ncc;


import com.intellij.execution.ui.CommonProgramParametersPanel;
import com.intellij.openapi.fileChooser.FileChooserDescriptor;
import com.intellij.openapi.fileChooser.FileChooserDescriptorFactory;
import com.intellij.openapi.ui.LabeledComponent;
import com.intellij.openapi.ui.TextFieldWithBrowseButton;
import com.intellij.ui.MacroAwareTextBrowseFolderListener;
import com.intellij.ui.RawCommandLineEditor;

import javax.swing.*;
import java.awt.*;

public class NccConfigForm extends CommonProgramParametersPanel {

    private LabeledComponent<JComponent> interpreterPathComponent;
    private TextFieldWithBrowseButton interpreterPathField;

    private LabeledComponent<JComponent> python3PathComponent;
    private TextFieldWithBrowseButton python3PathField;

    private LabeledComponent<JComponent> scriptNameComponent;
    private TextFieldWithBrowseButton scriptNameField;

    public NccConfigForm() {
    }

    protected void initOwnComponents() {

        FileChooserDescriptor chooseInterpreterDescriptor = FileChooserDescriptorFactory.createSingleLocalFileDescriptor();
        chooseInterpreterDescriptor.setTitle("Choose interpreter...");

        interpreterPathField = new TextFieldWithBrowseButton();
        interpreterPathField.addBrowseFolderListener(new MacroAwareTextBrowseFolderListener(chooseInterpreterDescriptor, getProject()));
        interpreterPathComponent = LabeledComponent.create(createComponentWithMacroBrowse(interpreterPathField), "Interpreter path:");
        interpreterPathComponent.setLabelLocation(BorderLayout.WEST);

        FileChooserDescriptor choosePython3Descriptor = FileChooserDescriptorFactory.createSingleLocalFileDescriptor();
        choosePython3Descriptor.setTitle("Choose Python...");

        python3PathField = new TextFieldWithBrowseButton();
        python3PathField.addBrowseFolderListener(new MacroAwareTextBrowseFolderListener(choosePython3Descriptor, getProject()));
        python3PathComponent = LabeledComponent.create(createComponentWithMacroBrowse(python3PathField), "Python path:");
        python3PathComponent.setLabelLocation(BorderLayout.WEST);


        FileChooserDescriptor chooseScriptDescriptor = FileChooserDescriptorFactory.createSingleLocalFileDescriptor();
        scriptNameField = new TextFieldWithBrowseButton();
        scriptNameField.addBrowseFolderListener(new MacroAwareTextBrowseFolderListener(chooseScriptDescriptor, getProject()));

        scriptNameComponent = LabeledComponent.create(createComponentWithMacroBrowse(scriptNameField), "Script:");
        scriptNameComponent.setLabelLocation(BorderLayout.WEST);
    }


    @Override
    protected void addComponents() {
        initOwnComponents();

        add(scriptNameComponent);
        add(python3PathComponent);
        add(interpreterPathComponent);

        super.addComponents();

        remove(myWorkingDirectoryField);
    }

    public void resetBash(NccRunConfiguration configuration) {
        python3PathField.setText(configuration.getPython3Path());
        interpreterPathField.setText(configuration.getInterpreterPath());
        scriptNameField.setText(configuration.getScriptName());
    }

    public void applyBashTo(NccRunConfiguration configuration) {
        configuration.setPython3Path(python3PathField.getText());
        configuration.setInterpreterPath(interpreterPathField.getText());
        configuration.setScriptName(scriptNameField.getText());
    }
}