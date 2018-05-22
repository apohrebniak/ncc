package com.apo.ncc;

import com.intellij.openapi.options.ConfigurationException;
import com.intellij.openapi.options.SettingsEditor;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class NccSettingsEditor extends SettingsEditor<NccRunConfiguration> {
    private NccConfigForm form;

    public NccSettingsEditor() {
        this.form = new NccConfigForm();
    }

    @Override
    protected void resetEditorFrom(NccRunConfiguration demoRunConfiguration) {
        form.reset(demoRunConfiguration);
        form.resetBash(demoRunConfiguration);
    }

    @Override
    protected void applyEditorTo(NccRunConfiguration demoRunConfiguration) throws ConfigurationException {
        form.applyTo(demoRunConfiguration);
        form.applyBashTo(demoRunConfiguration);
    }

    @NotNull
    @Override
    protected JComponent createEditor() {
        return form;
    }
}
