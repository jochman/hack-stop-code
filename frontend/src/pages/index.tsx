import {
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  makeStyles,
  Typography,
  Collapse,
  MenuItem,
  Select,

} from '@material-ui/core';
import { Field, FieldArray, Form, Formik } from 'formik';
import { CheckboxWithLabel, TextField } from 'formik-material-ui';
import React, { Children, Component } from 'react';
import { array, boolean, number, object, string, ValidationError } from 'yup';

import { Integartion } from '../schema/integration';
import { Command } from '../schema/command';
import { Param } from '../schema/param';
import { Menu, TurnedInTwoTone } from '@material-ui/icons';
import axios from 'axios';
import YAML from 'yaml'
import fileDownload from 'js-file-download'




const emptyParam: Param =
{
  "key": "",
  "value": "",
  "required": false,
  "hidden": false,
}

const emptyCommand: Command =
{
  "name": "",
  "method": "GET",
  "suffix": "",
  "params": [emptyParam],
  "headers": [emptyParam],
  "body": ""
}

const initialValues: Integartion = {
  configuration: {
    name: "",
    base_url: "",
    context_key: "",
    headers: [emptyParam],
  },
  commands: [emptyCommand]
};


const useStyles = makeStyles((theme) => ({
  errorColor: {
    color: theme.palette.error.main,
  },
  noWrap: {
    [theme.breakpoints.up('sm')]: {
      flexWrap: 'nowrap',
    },
  },
}));



export default function Home() {

  const classes = useStyles();
  return (
    <Card>
      <CardContent>
        <Formik
          initialValues={initialValues}
          // initialValues={{
          //   fullName: '',
          //   donationsAmount: 0,
          //   termsAndConditions: false,
          //   donations: [emptyDonation],
          // }}
          // validationSchema={object({
          //   fullName: string()
          //     .required('Your name is required')
          //     .min(2, 'Your name needs to be at least 3 characters')
          //     .max(10, 'Your name needs to be at most 10 characters'),
          //   donationsAmount: number().required().min(10),
          //   termsAndConditions: boolean().required().isTrue(),
          //   donations: array(
          //     object({
          //       institution: string()
          //         .required('Institution name needed')
          //         .min(3, 'Institution name needs to be at least 3 characters')
          //         .max(
          //           10,
          //           'Institution name needs to be at most 10 characters'
          //         ),
          //       percentage: number()
          //         .required('Percentage needed')
          //         .min(1, 'Percentage needs to be at least 1%')
          //         .max(100, 'Percentage can be at most 100%'),
          //     })
          //   )
          //     .min(1, 'You need to provide at least 1 institution')
          //     .max(3, 'You can only provide 3 institution')
          //     .test((donations) => {
          //       const sum = donations?.reduce(
          //         (acc, curr) => acc + (curr.percentage || 0),
          //         0
          //       );

          //       if (sum !== 100) {
          //         return new ValidationError(
          //           `Percentage should be 100%, but you have ${sum}%`,
          //           undefined,
          //           'donations'
          //         );
          //       }

          //       return true;
          //     }),
          // })}
          onSubmit={async (values) => {
            console.log('my values', values);
            postData(values)
            return new Promise((res) => setTimeout(res, 2500));
          }}
        >
          {({ values, errors, isSubmitting, isValid }) => (
            <Form autoComplete="off">
              <Grid container direction="column" spacing={2}>
                <Grid item>
                  <Field
                    fullwidth="true"
                    name="configuration.name"
                    component={TextField}
                    label="Integration Name"
                  />
                </Grid>

                <Grid item>
                  <Field
                    fullwidth="true"
                    name="configuration.base_url"
                    component={TextField}
                    label="Base URL"
                  />
                </Grid>

                <Grid item>
                  <Field
                    fullwidth="true"
                    name="configuration.context_key"
                    component={TextField}
                    label="Context key"
                  />
                </Grid>



                <FieldArray name="configuration.headers">
                  {({ push, remove }) => (
                    <React.Fragment>
                      <Grid item>
                        <Typography variant="body2">
                          Your headers
                        </Typography>
                      </Grid>

                      {values.configuration.headers.map((_, header_index) => (
                        <Grid
                          container
                          item
                          className={classes.noWrap}
                          key={header_index}
                          spacing={2}
                        >
                          <Grid item container spacing={2} xs={12} sm="auto">
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`configuration.headers.${header_index}.key`}
                                component={TextField}
                                label="Header key"
                              />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`configuration.headers.${header_index}.value`}
                                component={TextField}
                                label="Header value"
                              />
                            </Grid>
                          </Grid>

                          <Grid item xs={12} sm="auto">
                            <Button
                              disabled={isSubmitting}
                              onClick={() => remove(header_index)}
                            >
                              Delete Header
                            </Button>
                          </Grid>
                        </Grid>

                      ))}
                      <Grid item>
                        <Button
                          disabled={isSubmitting}
                          variant="contained"
                          onClick={() => push(emptyParam)}
                        >
                          Add Header
                        </Button>
                      </Grid>
                    </React.Fragment>
                  )}
                </FieldArray>





                <FieldArray name="commands">
                  {({ push, remove }) => (
                    <React.Fragment>
                      <Grid item>
                        <Typography variant="body2">
                          All your commands
                        </Typography>
                      </Grid>

                      {values.commands.map((_, index) => (
                        <Grid
                          container
                          item
                          className={classes.noWrap}
                          key={index}
                          spacing={2}
                        >
                          <Grid item container spacing={2} xs={12} sm="auto">
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`commands.${index}.name`}
                                component={TextField}
                                label="Command Name"
                              />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`commands.[${index}].method`}
                                component={"select"}
                                placeholder="GET"
                                label="Command Method"
                              >
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                                <option value="DELETE">DELETE</option>
                                <option value="PUT">PUT</option>
                                <option value="PATCH">PATCH</option>

                              </Field>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`commands.[${index}].suffix`}
                                component={TextField}
                                type="string"
                                label="Command Suffix"
                              />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <Field
                                fullwidth="true"
                                name={`commands.[${index}].body`}
                                component={TextField}
                                type="string"
                                label="Command body"
                              />
                            </Grid>
                            <FieldArray name={`commands[${index}].params`}>
                              {({ push, remove }) => (
                                <React.Fragment>
                                  <Grid item>
                                    <Typography variant="body2">
                                      Params for command
                                    </Typography>
                                  </Grid>

                                  {values.commands[index].params.map((_, param_index) => (
                                    <Grid
                                      container
                                      item
                                      className={classes.noWrap}
                                      key={param_index}
                                      spacing={2}
                                    >
                                      <Grid item container spacing={2} xs={12} sm="auto">
                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].params.[${param_index}].key`}
                                            component={TextField}
                                            label="Param key"
                                          />
                                        </Grid>
                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].params.[${param_index}].value`}
                                            component={TextField}
                                            label="Param value"
                                          />
                                        </Grid>

                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].params.[${param_index}].required`}
                                            component={CheckboxWithLabel}
                                            type="checkbox"
                                            Label={{ "label": "Is required?" }}
                                          />
                                        </Grid>

                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].params.[${param_index}].hidden`}
                                            component={CheckboxWithLabel}
                                            type="checkbox"
                                            Label={{ "label": "Is hidden?" }}
                                          />
                                        </Grid>
                                      </Grid>

                                      <Grid item xs={12} sm="auto">
                                        <Button
                                          disabled={isSubmitting}
                                          onClick={() => remove(param_index)}
                                        >
                                          Delete param
                                        </Button>
                                      </Grid>
                                    </Grid>

                                  ))}
                                  <Grid item>
                                    <Button
                                      disabled={isSubmitting}
                                      variant="contained"
                                      onClick={() => push(emptyParam)}
                                    >
                                      Add Param
                                    </Button>
                                  </Grid>
                                </React.Fragment>
                              )}
                            </FieldArray>

                            <FieldArray name={`commands[${index}].headers`}>
                              {({ push, remove }) => (
                                <React.Fragment>
                                  <Grid item>
                                    <Typography variant="body2">
                                      Headers for command
                                    </Typography>
                                  </Grid>

                                  {values.commands[index].params.map((_, command_header_index) => (
                                    <Grid
                                      container
                                      item
                                      className={classes.noWrap}
                                      key={command_header_index}
                                      spacing={2}
                                    >
                                      <Grid item container spacing={2} xs={12} sm="auto">
                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].headers.[${command_header_index}].key`}
                                            component={TextField}
                                            label="Param key"
                                          />
                                        </Grid>
                                        <Grid item xs={12} sm={6}>
                                          <Field
                                            fullwidth="true"
                                            name={`commands.[${index}].headers.[${command_header_index}].value`}
                                            component={TextField}
                                            label="Param value"
                                          />
                                        </Grid>
                                      </Grid>

                                      <Grid item xs={12} sm="auto">
                                        <Button
                                          disabled={isSubmitting}
                                          onClick={() => remove(command_header_index)}
                                        >
                                          Delete Command Header
                                        </Button>
                                      </Grid>
                                    </Grid>

                                  ))}
                                  <Grid item>
                                    <Button
                                      disabled={isSubmitting}
                                      variant="contained"
                                      onClick={() => push(emptyParam)}
                                    >
                                      Add Command Header
                                    </Button>
                                  </Grid>
                                </React.Fragment>
                              )}
                            </FieldArray>


                          </Grid>

                          <Grid item xs={12} sm="auto">
                            <Button
                              disabled={isSubmitting}
                              onClick={() => remove(index)}
                            >
                              Delete Command
                            </Button>
                          </Grid>
                        </Grid>

                      ))}

                      <Grid item>
                        {typeof errors.commands === 'string' ? (
                          <Typography color="error">
                            {errors.commands}
                          </Typography>
                        ) : null}
                      </Grid>

                      <Grid item>
                        <Button
                          disabled={isSubmitting}
                          variant="contained"
                          onClick={() => push(emptyCommand)}
                        >
                          Add Command
                        </Button>
                      </Grid>
                    </React.Fragment>
                  )}
                </FieldArray>

                <Grid item>
                  <Button
                    disabled={isSubmitting}
                    type="submit"
                    variant="contained"
                    color="primary"
                    startIcon={
                      isSubmitting ? (
                        <CircularProgress size="0.9rem" />
                      ) : undefined
                    }
                  >
                    {isSubmitting ? 'Submitting' : 'Submit'}
                  </Button>
                </Grid>
              </Grid>

              <pre>{JSON.stringify({ values, errors }, null, 4)}</pre>
            </Form>
          )}
        </Formik>
      </CardContent>
    </Card >
  );
}

const postData = (values: any) => {
  axios.post("http://localhost:8000/", values).then((res: any) => {
    console.log(res.data)
    const doc = new YAML.Document();
    doc.contents = res.data;
    fileDownload(doc.toString(), 'integration.yml');



  })
}

