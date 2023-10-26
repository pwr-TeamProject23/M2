import { Formik, Field, Form, FormikHelpers } from "formik";
import React from "react";

interface Values {
  email: string;
  password: string;
}

function Styled(props: { children: React.ReactNode }) {
  return <div className="bg-stone-900">{props.children}</div>;
}

function Title() {
  return (
    <div className="text-3xl text-accent justify-self-center font-light pb-8">
      Log in to Reviewed
    </div>
  );
}

function SubmitButton() {
    return <div className="w-full grid p-8">
        <button type="submit" className="bg-accent px-4 py-2 text-light justify-self-center text-white">Submit</button>
    </div>
}

export default function LoginPage() {
  const onLoginSubmit = (
    values: Values,
    { setSubmitting }: FormikHelpers<Values>,
  ) => {};
  return (
    <div className="h-screen w-screen flex justify-center items-center bg-stone-100">
      <div className="flex-col grid items-center">
        <Title />
        <Formik
          initialValues={{
            email: "",
            password: "",
          }}
          onSubmit={onLoginSubmit}
        >
          <Form>
            <label htmlFor="email">Email</label>
            <Styled>
              <Field
                id="email"
                name="email"
                placeholder="your.name@pwr.edu.pl"
                type="email"
              />
            </Styled>

            <label htmlFor="password">Password</label>
            <Styled>
              <Field
                id="password"
                name="password"
                placeholder=""
                type="password"
              />
            </Styled>
            <SubmitButton/>
          </Form>
        </Formik>
      </div>
    </div>
  );
}
